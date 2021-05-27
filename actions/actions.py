import sqlite3
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, ActiveLoop, ActionExecuted
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import BotUttered

# 数据库地址
db_path = "data/example.db"


def get_email_data(email):
    """
    用户提供邮箱，然后从里面获取数据信息
    :param email:
    :return:
    """
    db = sqlite3.connect(db_path)
    cursor = db.cursor()
    sql1 = "SELECT * FROM orders WHERE order_email='{}'".format(email)
    cursor.execute(sql1)
    data = cursor.fetchone()
    return db, data


class ActionOrderStatus(Action):
    """
    自定义动作，查询订单状态，写完后需要去domain添加一下，不然无法识别
    """

    def name(self) -> Text:
        return "action_order_status"

    async def run(self, dispatcher: CollectingDispatcher, tracker: Tracker,
                  domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """
        动作正式运行的时候触发
        :param dispatcher: 调度器,用于获取/发送信息
        :param tracker: 追踪器，内置了get_slot方法，可以获取槽位
        :param domain:
        :return:
        """
        email = tracker.get_slot("email")
        db, data = get_email_data(email)
        if bool(data):
            data_list = list(data)
            dispatcher.utter_message(response="utter_order_status", status=data_list[5])

        else:
            dispatcher.utter_message(response="utter_no_order")
        db.close()
        return []


class ActionCancelOrder(Action):
    def name(self) -> Text:
        return "action_cancel_order"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("email")
        db, data = get_email_data(email)
        if not bool(data):
            dispatcher.utter_message(text="亲，取消失败。没有查询有关您的订单，请检查邮箱号是否拼写错误。")
        else:
            sql1 = "UPDATE orders SET status='已取消' WHERE order_email='{}'".format(email)
            cursor = db.cursor()
            cursor.execute(sql1)
            db.commit()
            cursor.close()
            db.close()
            dispatcher.utter_message(text="亲，您的订单已经取消成功。")
        return []


class ActionReturn(Action):
    """
    用于自定义动作，退货
    """
    def name(self) -> Text:
        return "action_return"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        email = tracker.get_slot("email")
        db, data = get_email_data(email)
        if not bool(data):
            dispatcher.utter_message(text="亲，退货失败。您的邮箱：{}没有购买记录。".format(email))
        elif data[-1] in ["已取消", "已退货"]:
            dispatcher.utter_message(text="亲，您的订单{}，不能再退货了哈。".format(data[-1]))
        elif data[-1] in ["运输中", "订单待处理"]:
            dispatcher.utter_message(text="查询到您的订单状态为：{}，本次无需退货。".format(data[-1]))
            sql1 = "UPDATE orders SET status='已取消' WHERE order_email='{}'".format(email)
            cursor = db.cursor()
            cursor.execute(sql1)
            db.commit()
            cursor.close()
            db.close()
            dispatcher.utter_message(text="已为您取消订单。")
        else:
            cursor = db.cursor()
            sql1 = "UPDATE orders SET status='已退货' where order_email= '{}'".format(email)
            cursor.execute(sql1)
            db.commit()
            cursor.close()
            db.close()
            dispatcher.utter_message(text="已为您的订单退货，稍后将有快递员上门，退货完成后您将收到您的退款。")
        return []


class ActionProductSearch(Action):
    def name(self) -> Text:
        return "action_product_search"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # connect to DB
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        # get slots and save as tuple
        size_list = tracker.get_slot("size")
        if isinstance(size_list, list):
            size = size_list[-1]
        else:
            size = size_list
        shoe = (tracker.get_slot("color"), size)
        # place cursor on correct row based on search criteria

        cursor.execute("SELECT * FROM inventory WHERE color=? AND size=?", shoe)
        # retrieve sqlite row
        data_row = cursor.fetchone()
        connection.close()
        if data_row:
            # 如果有货,让用户去判断，要不要来一双
            dispatcher.utter_message(response="utter_in_stock")
            return [ActiveLoop("order_shoes_form")]  # 激活表单
        else:
            # 如果没货
            dispatcher.utter_message(response="utter_no_stock")
            # 清空槽位，方便用户重新查询
            slots_to_reset = ["size", "color"]
            return [SlotSet(slot, None) for slot in slots_to_reset]


class GiveName(Action):
    def name(self) -> Text:
        return "action_give_name"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        evt = BotUttered(
            text="我的名字? 我叫小贝",
            metadata={
                "nameGiven": "bot"
            }
        )

        return [evt]


class ActionSurveySubmit(Action):
    """
    自定义action,用于问卷提交
    """
    def name(self) -> Text:
        return "action_survey_submit"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        feed_back = tracker.get_slot("open_feedback")
        if feed_back in ["没有", None]:
            dispatcher.utter_message(response="utter_survey_end")
            # 激活服务评价，清空槽位
            return [ActiveLoop("rate_form"), SlotSet("open_feedback", None)]
        else:
            # 激活反馈表单,并且清空槽位，从新填写
            return [ActiveLoop("feedback_form"), SlotSet("open_feedback", None)]


class ActionFeedBackSubmit(Action):
    def name(self) -> Text:
        return "action_feedback_submit"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(response="utter_feedback_form_open_feedback")
        # 激活服务评价
        return [ActiveLoop("rate_form")]


class ActionOrderShoes(Action):
    """
    订购鞋子，自定义服务
    """
    def name(self) -> Text:
        return "action_order_shoes"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        size_list = tracker.get_slot("size")
        color = tracker.get_slot("color")
        # intent = tracker.get_intent_of_latest_message()  # 获取最近意图
        # print(intent, type(intent))
        # print(tracker.events_after_latest_restart())
        # print(tracker.get_latest_entity_values("number"))
        # 判断是否有两个槽位
        if isinstance(size_list, list):
            if len(size_list) > 1:
                num = size_list[0]
                size = size_list[-1]
            else:
                dispatcher.utter_message(text="请问需要几双，多大码的")
                return [SlotSet("size", None), ActiveLoop("order_shoes_form")]
        else:
            dispatcher.utter_message(text="请问需要几双，多大码的")
            return [SlotSet("size", None), ActiveLoop("order_shoes_form")]
        dispatcher.utter_message(text=f"您订购的商品为：{num}双大小为{size}码的{color}鞋子。")
        dispatcher.utter_message(response="utter_confirm_order")
        return []


class ActionOrderShoesFinish(Action):
    """
    订单完成-自定义动作
    """
    def name(self) -> Text:
        return "action_order_shoes_finish"

    def run(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="您好，您的商品已经帮您下单了，请您耐心等待。")
        slots_to_reset = ["size", "color"]
        return [SlotSet(slot, None) for slot in slots_to_reset] + [ActiveLoop("survey_form")]
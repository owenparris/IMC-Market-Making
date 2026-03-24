from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List
import string

class Trader:
    
    POSITION_LIMITS = {'EMERALDS': 80, 'TOMATOES': 80}

    def bid(self):
        return 15
    
    def run(self, state: TradingState):
        print("traderData: " + state.traderData)
        print("Observations: " + str(state.observations))

        result = {}
        for product in state.order_depths:
            orders: List[Order] = []
            order_depth: OrderDepth = state.order_depths[product]
            asks = sorted(list(order_depth.sell_orders.items()))
            bids = sorted(list(order_depth.buy_orders.items()), reverse=True)
            pos = state.position.get(product, 0)
            limit = self.POSITION_LIMITS.get(product, 80)

            if product == 'EMERALDS':
                acceptable_price = 10000
            elif product == "TOMATOES" and len(asks) and len(bids):
                acceptable_price = (int(asks[0][0]) + int(bids[0][0])) // 2
            else:
                continue

            soft_limit = limit // 2         # 40  — full-size, tight spread zone
            danger_limit = int(limit * 0.9)  # 72  — one side only, wider spread

            if abs(pos) <= soft_limit:
                # Neutral zone: full size both sides, tight spread (edge=2 per LinearUtility join_edge)
                buy_size, sell_size = 10, 10
            elif abs(pos) <= danger_limit:
                # Skew zone: reduce deepening side, widen its spread
                if pos > 0:
                    buy_size, sell_size = 3, 10
                else:
                    buy_size, sell_size = 10, 3
            else:
                # Danger zone: one side only (jmerle: hard liquidation at boundary)
                if pos > 0:
                    buy_size, sell_size = 0, 10
                else:
                    buy_size, sell_size = 10, 0

            for i in range(len(order_depth.sell_orders)):
                ask, ask_amount = asks[i]
                if int(ask) < acceptable_price:
                    orders.append(Order(product, ask, -ask_amount))
                elif int(ask) == acceptable_price and pos < 0:
                    orders.append(Order(product, ask, -ask_amount))
                    break
                elif int(ask) > acceptable_price + 1:
                    if sell_size > 0:
                        orders.append(Order(product, ask - 1, -sell_size))
                    break
                else:
                    break
    
            for i in range(len(order_depth.buy_orders)):
                bid, bid_amount = bids[i]
                if int(bid) > acceptable_price:
                    orders.append(Order(product, bid, -bid_amount))
                elif int(bid) == acceptable_price and pos > 0:
                    orders.append(Order(product, bid, -bid_amount))
                    break
                elif int(bid) < acceptable_price - 1:
                    if buy_size > 0:
                        orders.append(Order(product, bid + 1, buy_size))
                    break
                else:
                    break

            result[product] = orders
    
        traderData = ""
        conversions = 0
        return result, conversions, traderData
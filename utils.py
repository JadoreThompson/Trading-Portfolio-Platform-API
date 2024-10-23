from datetime import datetime
from uuid import UUID

# Local
from db_models import Orders, Users
from dependencies import get_user, get_session
from exceptions import DoesNotExist
from models import TradeRequestBody

# SA
from sqlalchemy import select


async def get_trades(user: Users, trade_details: TradeRequestBody = None):

    try:
        async with get_session() as session:
            if trade_details is None:
                results = await session.execute(select(Orders).where(Orders.user == user))
                return [
                    {
                        key: (value if not isinstance(value, (datetime, UUID)) else str(value))
                        for key, value in vars(trade).items()
                        if value != None and key != '_sa_instance_state' and value != 'null'
                    }
                    for trade in results.scalars().all()
                ]

            query = select(Orders).where(Orders.user == user)

            if trade_details.is_active:
                query = query.where(Orders.is_active == trade_details.is_active)

            if trade_details.ticker:
                query = query.where(Orders.ticker == trade_details.ticker)

            if trade_details.min_dollar_amount:
                query = query.where(Orders.dollar_amount >= trade_details.min_dollar_amount)

            if trade_details.max_dollar_amount:
                query = query.where(Orders.dollar_amount <= trade_details.max_dollar_amount)

            if trade_details.min_unrealised_pnl:
                query = query.where(Orders.unrealised_pnl >= trade_details.min_unrealised_pnl)

            if trade_details.max_unrealised_pnl:
                query = query.where(Orders.unrealised_pnl <= trade_details.max_unrealised_pnl)

            if trade_details.min_realised_pnl:
                query = query.where(Orders.realised_pnl >= trade_details.min_realised_pnl)

            if trade_details.max_realised_pnl:
                query = query.where(Orders.realised_pnl <= trade_details.max_realised_pnl)

            if trade_details.min_open_price:
                query = query.where(Orders.open_price >= trade_details.min_open_price)

            if trade_details.max_open_price:
                query = query.where(Orders.open_price <= trade_details.max_open_price)

            if trade_details.min_close_price:
                query = query.where(Orders.close_price >= trade_details.min_close_price)

            if trade_details.max_close_price:
                query = query.where(Orders.close_price <= trade_details.max_close_price)

            if trade_details.open_start:
                query = query.where(Orders.created_at >= trade_details.open_start)

            if trade_details.open_end:
                query = query.where(Orders.created_at <= trade_details.open_end)

            if trade_details.close_start:
                query = query.where(Orders.closed_at >= trade_details.close_start)

            if trade_details.close_end:
                query = query.where(Orders.closed_at <= trade_details.close_end)

            if trade_details.order_type:
                query = query.where(Orders.order_type == trade_details.order_type)

            result = await session.execute(query)
            trades = result.scalars().all()

            return [
                {
                    key: (value if not isinstance(value, (datetime, UUID)) else str(value))
                    for key, value in vars(trade).items()
                    if value != None and key != '_sa_instance_state' and value != 'null'
                }
                for trade in trades
            ]
    except DoesNotExist:
        raise
    except Exception:
        raise

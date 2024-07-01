from django.urls import path
from stocks.views.last_quote import LastQuote
from stocks.views.history import HistoryData
from stocks.views.dividends import DividendsList
from stocks.views.splits import SplitsList
from stocks.views.options_history import OptionsHistoryData


urlpatterns = [
    path('last-quote', LastQuote.as_view(), name='last_quote'),
    path('history', HistoryData.as_view(), name='history_data'),
    path('dividends-list', DividendsList.as_view(), name='dividends_list'),
    path('splits-list', SplitsList.as_view(), name='splits_list'),
    path('options/history', OptionsHistoryData.as_view(), name='options_history_data'),
]

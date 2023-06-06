
def get_news_with_params(news, params):
    result = news
    bad_news = params.get('bad_news')
    if not bad_news is None:
        bad_news = int(bad_news)
        result = list(filter(lambda n: int(n.get('bad_news')) == bad_news, news))
    return result
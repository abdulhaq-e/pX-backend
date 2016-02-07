from collections import OrderedDict


def get_filter_params(request):

    params = OrderedDict()

    for key, val in request.query_params.iteritems():
        if key.startswith('filter[') and key.endswith(']'):
            field = key.replace('filter[', '').replace(']', '')
            params[field] = request.query_params[key]

    return params

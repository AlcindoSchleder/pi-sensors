# -*- coding: utf-8 -*-

RESULTS = {
    'status': {
        'sttCode': 200,
        'sttMsgs': ''
    },
    'data': None,
    'message': '',
    'origin': ''
}


class DictionaryUtility:
    """
    Utility methods for dealing with dictionaries.
    """
    @staticmethod
    def to_object(item):
        """
        Convert a dictionary to an object (recursive).
        """
        def convert(obj: object = None) -> object:
            if obj is None:
                return None
            if isinstance(obj, dict):
                return type('jo', (), {k: convert(v) for k, v in obj.items()})
            if isinstance(obj, list):
                def yield_convert(obj_list):
                    for index, value in enumerate(obj_list):
                        yield convert(value)
                return list(yield_convert(obj))
            else:
                return obj

        return convert(item)

    @staticmethod
    def get_result() -> object:
        return DictionaryUtility.to_object(RESULTS)

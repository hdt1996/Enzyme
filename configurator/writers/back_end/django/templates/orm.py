from .....modules.Utilities.py.util import *
from ...utils.utils import StringModify
import inspect

class ChoiceORM():
    def __init__(self):
        self.options=\
        (inspect.cleandoc(
        """
            QUERY_OPTIONS = \\
            {
                'greater':'__gt',
                'greater-equal':'__gte',
                'lesser':'__lt',
                'lesser-equal':'__lte',
                'startswith':'__name__startswith',
                'contains':'__name__contains',
                'in':'__in',
                'equal':''
            }
        """),[])

        self.validateSelector =\
        (inspect.cleandoc(
        """
            if selectors == None:
                return Response({{'Selector_Error':'No Search Parameters passed in'}}, status = status.HTTP_403_FORBIDDEN)
            fixed_query = {fixed_query}
            for field in selectors:
                if field in fixed_query:
                    return Response({{'Selector_Error':'Custom field passed into non-custom field'}}, status = status.HTTP_403_FORBIDDEN)
            sel_dict = {{}}
            for field in fixed_query:
                oper = fixed_query[field]['operator']
                value = fixed_query[field]['value']
                sel_dict[f"{{field}}{{QUERY_OPTIONS[oper]}}"] = value

        """
        ),[])

        self.queries =\
        {
            'custom_query':
            (inspect.cleandoc(
            """
                allowed_fields = {fields}
                if isinstance(selectors, dict):
                    for field in selectors:
                        oper = selectors[field]['operator']
                        value = selectors[field]['value']
                        if oper in QUERY_OPTIONS:
                            sel_dict[f"{{field}}{{QUERY_OPTIONS[oper]}}"] = value
                        if field not in allowed_fields:
                            return Response({{'Selector_Error':'Unallowed field passed in'}}, status = status.HTTP_403_FORBIDDEN)
                else:
                    raise TypeError("Data Type Invalid: Only dictionary objects are allowed.")
                {user_select}
                table_query = {table}.objects.filter(**sel_dict)
                if len(table_query) == 0:
                    return Response({{'Empty':'No Data'}}, status = status.HTTP_200_OK)
            """),[]),

            'user':
            (inspect.cleandoc(
            """
                user_query = User.objects.filter(username = request.user)
                if len(user_query) == 0:
                    return Response({'Error':"User does not exist"})
                active_user = user_query[0]
            """),[]),

            'fixed_query':
            (inspect.cleandoc(
            """
                if isinstance(selectors, dict):
                    for field in selectors:
                        oper = selectors[field]['operator']
                        value = selectors[field]['value']
                        if oper in QUERY_OPTIONS:
                            sel_dict[f"{{field}}{{QUERY_OPTIONS[oper]}}"] = value
                else:
                    raise TypeError("Data Type Invalid: Only dictionary objects are allowed.")
                {user_select}
                table_query = {table}.objects.filter(**sel_dict)
                if len(table_query) == 0:
                    return Response({{'Empty':'No Data'}}, status = status.HTTP_200_OK)
            """),[])
            } 


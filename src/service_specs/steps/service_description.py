# Copyright (C) 2013 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
# Created By: david@reciprocitylabs.com
# Maintained By: david@reciprocitylabs.com

from behave import given, then
from tests.ggrc.behave.utils import get_resource

@then('all expected endpoints are listed and GETtable in "{resource_name}"')
def validate_service_description(context, resource_name):
  service_description = getattr(context, resource_name)
  service_description_obj = service_description.get(
      u'service_description', None)
  assert service_description_obj is not None, \
      'Expected to find a service_description object in {0}\n{1}'.format(
          resource_name, service_description)
  endpoints = service_description_obj.get(u'endpoints', None)
  assert endpoints is not None, \
      'Expected to find service_description.endpoints in {0}\n{1}'.format(
          resource_name, service_description_obj)
  for endpoint_row in context.table:
    endpoint_name = endpoint_row['endpoint']
    max_query_count = int(endpoint_row['max_query_count'])
    endpoint_obj = endpoints.get(unicode(endpoint_name), None)
    assert endpoint_obj is not None, \
        'Expected to find service_description.endpoints.{0} in {1}\n{2}'.format(
            endpoint_name, resource_name, service_description)
    href = endpoint_obj.get('href', None)
    assert href is not None, \
        'Expected endpoint {0} to contain "href" value'.format(
            endpoint_name)
    query_count = context.query_count
    response = get_resource(context, href)
    if max_query_count > 0:
      assert (context.query_count - query_count) <= max_query_count, \
          'GET of {0} required {1} queries, which is more than {2}'\
            .format(href, context.query_count - query_count, max_query_count)
    assert response.status_code == 200, \
        'Expected status code 200 on GET of endpoint {0} URL {1}, received {2}'\
          .format(response.status_code)

@given('service description')
def place_service_description_into_context(context):
  context.execute_steps(u'When GET of "/api" as "service_description"')

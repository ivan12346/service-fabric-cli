# -----------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# -----------------------------------------------------------------------------

"""Custom parameter handling for commands"""
from __future__ import print_function
import json
from knack.arguments import ArgumentsContext, CLIArgumentType


def json_encoded(arg_str):
    """Convert from argument JSON string to complex object.
    This function also accepts a file path to a .txt file containing the JSON string.
    File paths should be prefixed by '@'
    Path can be relative path or absolute path."""

    if arg_str and arg_str[0] == '@':
        try:
            with open(arg_str[1:], 'r') as json_file:
                json_str = json_file.read()
                return json.loads(json_str)
        except IOError:
            # This is the error that python 2.7 returns on no file found
            print('File not found at {0}'.format(arg_str[1:]))
        except ValueError as ex:
            print('Decoding JSON value from file {0} failed: \n{1}'.format(arg_str[1:], ex))
            raise

    try:
        return json.loads(arg_str)
    except ValueError as ex:
        print('Loading JSON from string input failed. '
              'You can also pass the json argument in a .txt file. \n'
              'To do so, set argument value to the absolute path of the text file '
              'prefixed by "@". \nIf you have passed in a file name, please ensure that the JSON '
              'is correct. Error: \n{0}'.format(ex))
        raise


def custom_arguments(self, _):  # pylint: disable=too-many-statements
    """Load specialized arguments for commands"""

    with ArgumentsContext(self, '') as arg_context:  # Global argument
        arg_context.argument('timeout', type=int, options_list=('-t', '--timeout'))

    # When the options_list is provided either for this timeout or the global timeout, the text
    # in the help file is ignored, so we are putting the help text here instead.
    with ArgumentsContext(self, 'application upload') as arg_context:
        arg_context.argument('timeout', type=int, options_list=('-t', '--timeout'),
                             help='The total timeout in seconds. '
                                  'Upload will fail and return error after the upload timeout '
                                  'duration has passed. This timeout applies to '
                                  'the entire application package, and individual file timeouts '
                                  'will equal the remaining timeout duration. '
                                  'Timeout does not include the time required to '
                                  'compress the application package. ')

    with ArgumentsContext(self, 'application create') as arg_context:
        arg_context.argument('parameters', type=json_encoded)
        arg_context.argument('metrics', type=json_encoded)
        arg_context.argument('min_node_count', type=int)
        arg_context.argument('max_node_count', type=int)

    with ArgumentsContext(self, 'application deployed-list') as arg_context:
        arg_context.argument('max_results', type=int)

    with ArgumentsContext(self, 'node list') as arg_context:
        arg_context.argument('max_results', type=int)

    with ArgumentsContext(self, 'application list') as arg_context:
        arg_context.argument('application_definition_kind_filter', type=int)
        arg_context.argument('max_results', type=int)

    with ArgumentsContext(self, 'application upgrade') as arg_context:
        arg_context.argument('parameters', type=json_encoded)
        arg_context.argument('default_service_health_policy',
                             type=json_encoded)
        arg_context.argument('service_health_policy', type=json_encoded)
        arg_context.argument('replica_set_check_timeout', type=int)
        arg_context.argument('max_unhealthy_apps', type=int)

    with ArgumentsContext(self, 'service create') as arg_context:
        arg_context.argument('instance_count', type=int)
        arg_context.argument('target_replica_set_size', type=int)
        arg_context.argument('min_replica_set_size', type=int)
        arg_context.argument('replica_restart_wait', type=int)
        arg_context.argument('quorum_loss_wait', type=int)
        arg_context.argument('stand_by_replica_keep', type=int)
        arg_context.argument('load_metrics', type=json_encoded)
        arg_context.argument('placement_policy_list', type=json_encoded)
        arg_context.argument('scaling_policies', type=json_encoded)

    with ArgumentsContext(self, 'service update') as arg_context:
        arg_context.argument('instance_count', type=int)
        arg_context.argument('target_replica_set_size', type=int)
        arg_context.argument('min_replica_set_size', type=int)
        arg_context.argument('load_metrics', type=json_encoded)
        arg_context.argument('scaling_policies', type=json_encoded)

    with ArgumentsContext(self, 'chaos start') as arg_context:
        arg_context.argument('app_type_health_policy_map', type=json_encoded)
        arg_context.argument('max_cluster_stabilization', type=int)
        arg_context.argument('max_concurrent_faults', type=int)
        arg_context.argument('wait_time_between_faults', type=int)
        arg_context.argument('wait_time_between_iterations', type=int)
        arg_context.argument('max_percent_unhealthy_nodes', type=int)
        arg_context.argument('max_percent_unhealthy_apps', type=int)
        arg_context.argument('context', type=json_encoded)
        arg_context.argument('chaos_target_filter', type=json_encoded)

    with ArgumentsContext(self, 'chaos schedule set') as arg_context:
        arg_context.argument('version', type=int)
        arg_context.argument('chaos_parameters_dictionary', type=json_encoded)
        arg_context.argument('jobs', type=json_encoded)

    with ArgumentsContext(self, 'cluster health') as arg_context:
        arg_context.argument('nodes_health_state_filter', type=int)
        arg_context.argument('applications_health_state_filter', type=int)
        arg_context.argument('events_health_state_filter', type=int)

    with ArgumentsContext(self, 'node health') as arg_context:
        arg_context.argument('events_health_state_filter', type=int)

    with ArgumentsContext(self, 'application health') as arg_context:
        arg_context.argument('events_health_state_filter', type=int)
        arg_context.argument('deployed_applications_health_state_filter',
                             type=int)
        arg_context.argument('services_health_state_filter', type=int)

    with ArgumentsContext(self, 'application deployed-list') as arg_context:
        arg_context.argument('max_results', type=int)

    with ArgumentsContext(self, 'application deployed-health') as arg_context:
        arg_context.argument('events_health_state_filter', type=int)
        arg_context.argument('deployed_service_packages_health_state_filter',
                             type=int)

    with ArgumentsContext(self, 'service health') as arg_context:
        arg_context.argument('events_health_state_filter', type=int)
        arg_context.argument('partitions_health_state_filter', type=int)

    with ArgumentsContext(self, 'service resolve') as arg_context:
        arg_context.argument('partition_key_type', type=int)

    with ArgumentsContext(self, 'partition health') as arg_context:
        arg_context.argument('events_health_state_filter', type=int)
        arg_context.argument('replicas_health_state_filter', type=int)

    with ArgumentsContext(self, 'replica health') as arg_context:
        arg_context.argument('events_health_state_filter', type=int)

    with ArgumentsContext(self, 'service package-health') as arg_context:
        arg_context.argument('events_health_state_filter', type=int)

    with ArgumentsContext(self, 'partition quorum-loss') as arg_context:
        arg_context.argument('quorum_loss_duration', type=int)

    with ArgumentsContext(self, 'node transition') as arg_context:
        arg_context.argument('stop_duration_in_seconds', type=int)

    with ArgumentsContext(self, 'cluster operation-list') as arg_context:
        arg_context.argument('type_filter', type=int)
        arg_context.argument('state_filter', type=int)

    with ArgumentsContext(self, 'application type-list') as arg_context:
        arg_context.argument('max_results', type=int)
        arg_context.argument('application_type_definition_kind_filter',
                             type=int)

    with ArgumentsContext(self, 'application type') as arg_context:
        arg_context.argument('max_results', type=int)

    with ArgumentsContext(self, 'compose list') as arg_context:
        arg_context.argument('max_results', type=int)

    with ArgumentsContext(self, 'cluster upgrade') as arg_context:
        arg_context.argument('replica_set_check_timeout', type=int)
        arg_context.argument('unhealthy_nodes', type=int)
        arg_context.argument('unhealthy_applications', type=int)
        arg_context.argument('app_type_health_map', type=json_encoded)
        arg_context.argument('delta_unhealthy_nodes', type=int)
        arg_context.argument('upgrade_domain_delta_unhealthy_nodes', type=int)
        arg_context.argument('app_health_map', type=json_encoded)

    with ArgumentsContext(self, 'sa-cluster config-upgrade') as arg_context:
        arg_context.argument('unhealthy_applications', type=int)
        arg_context.argument('unhealthy_nodes', type=int)
        arg_context.argument('delta_unhealthy_nodes', type=int)
        arg_context.argument('upgrade_domain_delta_unhealthy_nodes', type=int)
        arg_context.argument('application_health_policies', type=json_encoded)

    with ArgumentsContext(self, 'cluster upgrade-update') as arg_context:
        arg_context.argument('replica_set_check_timeout', type=int)
        arg_context.argument('unhealthy_nodes', type=int)
        arg_context.argument('unhealthy_applications', type=int)
        arg_context.argument('app_type_health_map', type=json_encoded)
        arg_context.argument('delta_unhealthy_nodes', type=int)
        arg_context.argument('upgrade_domain_delta_unhealthy_nodes', type=int)
        arg_context.argument('app_health_map', type=json_encoded)

    with ArgumentsContext(self, 'rpm list') as arg_context:
        arg_context.argument('state_filter', type=int)

    with ArgumentsContext(self, 'compose upgrade') as arg_context:
        arg_context.argument('unhealthy_app', type=int)
        arg_context.argument('default_svc_type_health_map', type=json_encoded)
        arg_context.argument('svc_type_health_map', type=json_encoded)

    with ArgumentsContext(self, 'property put') as arg_context:
        arg_context.argument('value', type=json_encoded)

    with ArgumentsContext(self, 'is') as arg_context:
        # expect the parameter command_input in the python method as --command in commandline.
        arg_context.argument('command_input',
                             CLIArgumentType(options_list='--command'))

    with ArgumentsContext(self, 'mesh') as arg_context:
        arg_context.argument('application_resource_name',
                             options_list=('--app-name', '--application-name'),
                             help="The name of the application")
        arg_context.argument('service_resource_name', options_list=('--service-name'),
                             help="The name of the service")

    with ArgumentsContext(self, 'mesh app') as arg_context:
        arg_context.argument('application_resource_name', options_list=('--name', '-n'),
                             help="The name of the application")

    with ArgumentsContext(self, 'mesh service') as arg_context:
        arg_context.argument('service_resource_name', options_list=('--name', '-n'),
                             help="The name of the service")

    with ArgumentsContext(self, 'mesh service-replica') as arg_context:
        arg_context.argument('replica_name', options_list=('--name', '-n'),
                             help="The name of the service replica")

    with ArgumentsContext(self, 'mesh codepackage') as arg_context:
        arg_context.argument('code_package_name', options_list=('--name', '-n'),
                             help="The name of the code package")

    with ArgumentsContext(self, 'mesh network') as arg_context:
        arg_context.argument('network_resource_name', options_list=('--name', '-n'),
                             help="The name of the network")

    with ArgumentsContext(self, 'mesh volume') as arg_context:
        arg_context.argument('volume_resource_name', options_list=('--name', '-n'),
                             help="The name of the volume")

    with ArgumentsContext(self, 'mesh service-replica') as arg_context:
        arg_context.argument('replica_name', options_list=('--name', '-n'),
                             help="The name of the service replica")

    with ArgumentsContext(self, 'mesh secret') as arg_context:
        arg_context.argument('secret_resource_name', options_list=('-n', '--name'),
                             help="The name of the secret resource")

    with ArgumentsContext(self, 'mesh secretvalue') as arg_context:
        arg_context.argument('secret_resource_name', options_list=('-n', '--secret-name'),
                             help="The name of the secret resource")
        arg_context.argument('secret_value_resource_name', options_list=('-v', '--version'),
                             help="The name of the secret version")

    with ArgumentsContext(self, 'mesh gateway') as arg_context:
        arg_context.argument('gateway_resource_name',
                             options_list=('-n', '--name'),
                             help="The name of the gateway resource")
    with ArgumentsContext(self, 'mesh deployment create') as arg_context:
        from argcomplete.completers import FilesCompleter
        arg_context.argument('parameters', action='append', nargs='+', completer=FilesCompleter())

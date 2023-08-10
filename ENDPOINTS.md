**THIS FILE IS AUTO-GENERATED DO NOT EDIT**

All URIs are relative to */dataservice*
HTTP request | Supported Versions | Method | Payload Type | Return Type | Tenancy Mode
------------ | ------------------ | ------ | ------------ | ----------- | ------------
POST /admin/user||[**AdministrationUserAndGroup.create_user**](vmngclient/endpoints/administration_user_and_group.py#L157)|[**User**](vmngclient/endpoints/administration_user_and_group.py#L11)||
POST /admin/usergroup||[**AdministrationUserAndGroup.create_user_group**](vmngclient/endpoints/administration_user_and_group.py#L161)|[**UserGroup**](vmngclient/endpoints/administration_user_and_group.py#L48)||
DELETE /admin/user/{username}||[**AdministrationUserAndGroup.delete_user**](vmngclient/endpoints/administration_user_and_group.py#L173)|||
DELETE /admin/usergroup/{group_name}||[**AdministrationUserAndGroup.delete_user_group**](vmngclient/endpoints/administration_user_and_group.py#L177)|||
GET /admin/user/userAuthType||[**AdministrationUserAndGroup.find_user_auth_type**](vmngclient/endpoints/administration_user_and_group.py#L193)||[**UserAuthType**](vmngclient/endpoints/administration_user_and_group.py#L37)|
GET /admin/usergroup||[**AdministrationUserAndGroup.find_user_groups**](vmngclient/endpoints/administration_user_and_group.py#L197)||DataSequence[[**UserGroup**](vmngclient/endpoints/administration_user_and_group.py#L48)]|
GET /admin/user/role||[**AdministrationUserAndGroup.find_user_role**](vmngclient/endpoints/administration_user_and_group.py#L205)||[**UserRole**](vmngclient/endpoints/administration_user_and_group.py#L33)|
GET /admin/user||[**AdministrationUserAndGroup.find_users**](vmngclient/endpoints/administration_user_and_group.py#L209)||DataSequence[[**User**](vmngclient/endpoints/administration_user_and_group.py#L11)]|
GET /admin/user/activeSessions||[**AdministrationUserAndGroup.get_active_sessions**](vmngclient/endpoints/administration_user_and_group.py#L213)||DataSequence[[**ActiveSession**](vmngclient/endpoints/administration_user_and_group.py#L89)]|
DELETE /admin/user/removeSessions||[**AdministrationUserAndGroup.remove_sessions**](vmngclient/endpoints/administration_user_and_group.py#L225)|[**SessionsDeleteRequest**](vmngclient/endpoints/administration_user_and_group.py#L105)|[**InvalidateSessionMessage**](vmngclient/endpoints/administration_user_and_group.py#L118)|
POST /admin/user/reset||[**AdministrationUserAndGroup.reset_user**](vmngclient/endpoints/administration_user_and_group.py#L229)|[**UserResetRequest**](vmngclient/endpoints/administration_user_and_group.py#L85)||
GET /admin/resourcegroup||[**AdministrationUserAndGroup.find_resource_groups**](vmngclient/endpoints/administration_user_and_group.py#L233)||DataSequence[[**ResourceGroup**](vmngclient/endpoints/administration_user_and_group.py#L127)]|
POST /admin/resourcegroup/switch||[**AdministrationUserAndGroup.switch_resource_group**](vmngclient/endpoints/administration_user_and_group.py#L237)|[**ResourceGroupSwitchRequest**](vmngclient/endpoints/administration_user_and_group.py#L144)||
PUT /admin/resourcegroup/{group_id}||[**AdministrationUserAndGroup.update_resource_group**](vmngclient/endpoints/administration_user_and_group.py#L241)|[**ResourceGroupUpdateRequest**](vmngclient/endpoints/administration_user_and_group.py#L137)||
DELETE /admin/resourcegroup/{group_id}||[**AdministrationUserAndGroup.delete_resource_group**](vmngclient/endpoints/administration_user_and_group.py#L245)|||
POST /admin/resourcegroup||[**AdministrationUserAndGroup.create_resource_group**](vmngclient/endpoints/administration_user_and_group.py#L249)|[**ResourceGroup**](vmngclient/endpoints/administration_user_and_group.py#L127)||
PUT /admin/user/password/{username}||[**AdministrationUserAndGroup.update_password**](vmngclient/endpoints/administration_user_and_group.py#L261)|[**UserUpdateRequest**](vmngclient/endpoints/administration_user_and_group.py#L20)||
PUT /admin/user/profile/password||[**AdministrationUserAndGroup.update_profile_password**](vmngclient/endpoints/administration_user_and_group.py#L269)|[**ProfilePasswordUpdateRequest**](vmngclient/endpoints/administration_user_and_group.py#L122)||
PUT /admin/user/{username}||[**AdministrationUserAndGroup.update_user**](vmngclient/endpoints/administration_user_and_group.py#L273)|[**UserUpdateRequest**](vmngclient/endpoints/administration_user_and_group.py#L20)||
PUT /admin/usergroup/{group_name}||[**AdministrationUserAndGroup.update_user_group**](vmngclient/endpoints/administration_user_and_group.py#L277)|[**UserGroup**](vmngclient/endpoints/administration_user_and_group.py#L48)||
GET /setting/configuration/webserver/certificate||[**CertificateManagementVManage.show_info**](vmngclient/endpoints/certificate_management_vmanage.py#L43)||[**WebServerCertificateInfo**](vmngclient/endpoints/certificate_management_vmanage.py#L9)|
GET /client/server||[**Client.server**](vmngclient/endpoints/client.py#L65)||[**ServerInfo**](vmngclient/endpoints/client.py#L21)|
GET /client/server/ready||[**Client.server_ready**](vmngclient/endpoints/client.py#L69)||[**ServerReady**](vmngclient/endpoints/client.py#L60)|
GET /client/about||[**Client.about**](vmngclient/endpoints/client.py#L73)||[**AboutInfo**](vmngclient/endpoints/client.py#L49)|
GET /clusterManagement/tenancy/mode||[**ClusterManagement.get_tenancy_mode**](vmngclient/endpoints/cluster_management.py#L60)||[**TenancyMode**](vmngclient/endpoints/cluster_management.py#L16)|
GET /device/action/status/{task_id}||[**ConfigurationDashboardStatus.find_status**](vmngclient/endpoints/configuration_dashboard_status.py#L89)||[**TaskData**](vmngclient/endpoints/configuration_dashboard_status.py#L76)|
GET /device/action/status/tasks||[**ConfigurationDashboardStatus.find_running_tasks**](vmngclient/endpoints/configuration_dashboard_status.py#L93)||[**TasksData**](vmngclient/endpoints/configuration_dashboard_status.py#L84)|
GET /device/action/ztp/upgrade/setting||[**ConfigurationDeviceActions.get_ztp_upgrade_config_setting**](vmngclient/endpoints/configuration_device_actions.py#L74)||DataSequence[[**ZTPUpgradeSettings**](vmngclient/endpoints/configuration_device_actions.py#L10)]|
POST /device/action/software/package||[**ConfigurationDeviceSoftwareUpdate.install_pkg**](vmngclient/endpoints/configuration_device_software_update.py#L22)|[**SoftwarePackageUpdatePayload**](vmngclient/utils/upgrades_helper.py#L68)||
POST /template/device/config/config/||[**ConfigurationDeviceTemplate.get_device_configuration_preview**](vmngclient/endpoints/configuration_device_template.py#L19)|[**FeatureToCLIPayload**](vmngclient/endpoints/configuration_device_template.py#L10)|str|
GET /settings/configuration/{setting_type}||[**ConfigurationSettings.get_configuration_by_setting_type**](vmngclient/endpoints/configuration_settings.py#L208)||dict|
GET /settings/configuration/organization||[**ConfigurationSettings.get_organizations**](vmngclient/endpoints/configuration_settings.py#L212)||DataSequence[[**Organization**](vmngclient/endpoints/configuration_settings.py#L29)]|
GET /settings/configuration/device||[**ConfigurationSettings.get_devices**](vmngclient/endpoints/configuration_settings.py#L216)||DataSequence[[**Device**](vmngclient/endpoints/configuration_settings.py#L35)]|
GET /settings/configuration/emailNotificationSettings||[**ConfigurationSettings.get_email_notification_settings**](vmngclient/endpoints/configuration_settings.py#L220)||DataSequence[[**EmailNotificationSettings**](vmngclient/endpoints/configuration_settings.py#L40)]|
GET /settings/configuration/hardwarerootca||[**ConfigurationSettings.get_hardware_root_cas**](vmngclient/endpoints/configuration_settings.py#L224)||DataSequence[[**HardwareRootCA**](vmngclient/endpoints/configuration_settings.py#L44)]|
GET /settings/configuration/certificate||[**ConfigurationSettings.get_certificates**](vmngclient/endpoints/configuration_settings.py#L228)||DataSequence[[**Certificate**](vmngclient/endpoints/configuration_settings.py#L49)]|
GET /settings/configuration/vedgecloud||[**ConfigurationSettings.get_vedge_cloud**](vmngclient/endpoints/configuration_settings.py#L232)||DataSequence[[**VEdgeCloud**](vmngclient/endpoints/configuration_settings.py#L58)]|
GET /settings/configuration/banner||[**ConfigurationSettings.get_banners**](vmngclient/endpoints/configuration_settings.py#L236)||DataSequence[[**Banner**](vmngclient/endpoints/configuration_settings.py#L62)]|
GET /settings/configuration/proxyHttpServer||[**ConfigurationSettings.get_proxy_http_servers**](vmngclient/endpoints/configuration_settings.py#L240)||DataSequence[[**ProxyHTTPServer**](vmngclient/endpoints/configuration_settings.py#L66)]|
GET /settings/configuration/reverseproxy||[**ConfigurationSettings.get_reverse_proxies**](vmngclient/endpoints/configuration_settings.py#L244)||DataSequence[[**ReverseProxy**](vmngclient/endpoints/configuration_settings.py#L72)]|
GET /settings/configuration/cloudx||[**ConfigurationSettings.get_cloudx**](vmngclient/endpoints/configuration_settings.py#L248)||DataSequence[[**CloudX**](vmngclient/endpoints/configuration_settings.py#L76)]|
GET /settings/configuration/manageEncryptedPassword||[**ConfigurationSettings.get_manage_encrypted_password**](vmngclient/endpoints/configuration_settings.py#L252)||DataSequence[[**ManageEncryptedPassword**](vmngclient/endpoints/configuration_settings.py#L80)]|
GET /settings/configuration/cloudservices||[**ConfigurationSettings.get_cloudservices**](vmngclient/endpoints/configuration_settings.py#L256)||DataSequence[[**CloudServices**](vmngclient/endpoints/configuration_settings.py#L84)]|
GET /settings/configuration/clientSessionTimeout||[**ConfigurationSettings.get_client_session_timeout**](vmngclient/endpoints/configuration_settings.py#L260)||DataSequence[[**ClientSessionTimeout**](vmngclient/endpoints/configuration_settings.py#L94)]|
GET /settings/configuration/sessionLifeTime||[**ConfigurationSettings.get_session_life_time**](vmngclient/endpoints/configuration_settings.py#L264)||DataSequence[[**SessionLifeTime**](vmngclient/endpoints/configuration_settings.py#L99)]|
GET /settings/configuration/serverSessionTimeout||[**ConfigurationSettings.get_server_session_timeout**](vmngclient/endpoints/configuration_settings.py#L268)||DataSequence[[**ServerSessionTimeout**](vmngclient/endpoints/configuration_settings.py#L103)]|
GET /settings/configuration/maxSessionsPerUser||[**ConfigurationSettings.get_max_sessions_per_user**](vmngclient/endpoints/configuration_settings.py#L272)||DataSequence[[**MaxSessionsPerUser**](vmngclient/endpoints/configuration_settings.py#L107)]|
GET /settings/configuration/passwordPolicy||[**ConfigurationSettings.get_password_policy**](vmngclient/endpoints/configuration_settings.py#L276)||DataSequence[[**PasswordPolicy**](vmngclient/endpoints/configuration_settings.py#L111)]|
GET /settings/configuration/vmanagedatastream||[**ConfigurationSettings.get_vmanage_data_stream**](vmngclient/endpoints/configuration_settings.py#L280)||DataSequence[[**VManageDataStream**](vmngclient/endpoints/configuration_settings.py#L118)]|
GET /settings/configuration/dataCollectionOnNotification||[**ConfigurationSettings.get_data_collection_on_notification**](vmngclient/endpoints/configuration_settings.py#L284)||DataSequence[[**DataCollectionOnNotification**](vmngclient/endpoints/configuration_settings.py#L125)]|
GET /settings/configuration/sdWanTelemetry||[**ConfigurationSettings.get_sdwan_telemetry**](vmngclient/endpoints/configuration_settings.py#L288)||DataSequence[[**SDWANTelemetry**](vmngclient/endpoints/configuration_settings.py#L129)]|
GET /management/statsconfig||[**ConfigurationSettings.get_stats_config**](vmngclient/endpoints/configuration_settings.py#L292)||DataSequence[[**StatsOperation**](vmngclient/endpoints/configuration_settings.py#L133)]|
GET /settings/configuration/spMetadata||[**ConfigurationSettings.get_sp_metadata**](vmngclient/endpoints/configuration_settings.py#L296)||str|
GET /management/elasticsearch/index/size||[**ConfigurationSettings.get_elasticsearch_db_size**](vmngclient/endpoints/configuration_settings.py#L300)||DataSequence[[**ElasticSearchDBSize**](vmngclient/endpoints/configuration_settings.py#L147)]|
GET /settings/configuration/googleMapKey||[**ConfigurationSettings.get_google_map_key**](vmngclient/endpoints/configuration_settings.py#L304)||DataSequence[[**GoogleMapKey**](vmngclient/endpoints/configuration_settings.py#L152)]|
GET /settings/configuration/maintenanceWindow||[**ConfigurationSettings.get_maintenance_window**](vmngclient/endpoints/configuration_settings.py#L308)||DataSequence[[**MaintenanceWindow**](vmngclient/endpoints/configuration_settings.py#L140)]|
GET /settings/configuration/softwareMaintenance||[**ConfigurationSettings.get_software_install_timeout**](vmngclient/endpoints/configuration_settings.py#L312)||DataSequence[[**SoftwareInstallTimeout**](vmngclient/endpoints/configuration_settings.py#L156)]|
GET /settings/configuration/credentials||[**ConfigurationSettings.get_ips_signature_settings**](vmngclient/endpoints/configuration_settings.py#L316)||DataSequence[[**IPSSignatureSettings**](vmngclient/endpoints/configuration_settings.py#L161)]|
GET /settings/configuration/smartaccountcredentials||[**ConfigurationSettings.get_smart_account_credentials**](vmngclient/endpoints/configuration_settings.py#L320)||DataSequence[[**SmartAccountCredentials**](vmngclient/endpoints/configuration_settings.py#L169)]|
GET /settings/configuration/pnpConnectSync||[**ConfigurationSettings.get_pnp_connect_sync**](vmngclient/endpoints/configuration_settings.py#L324)||DataSequence[[**PnPConnectSync**](vmngclient/endpoints/configuration_settings.py#L174)]|
GET /settings/configuration/claimDevice||[**ConfigurationSettings.get_claim_device**](vmngclient/endpoints/configuration_settings.py#L328)||DataSequence[[**ClaimDevice**](vmngclient/endpoints/configuration_settings.py#L178)]|
GET /settings/configuration/walkme||[**ConfigurationSettings.get_walkme**](vmngclient/endpoints/configuration_settings.py#L332)||DataSequence[[**WalkMe**](vmngclient/endpoints/configuration_settings.py#L182)]|
GET /device/tier||[**MonitoringDeviceDetails.get_tiers**](vmngclient/endpoints/monitoring_device_details.py#L116)||DataSequence[[**Tier**](vmngclient/endpoints/monitoring_device_details.py#L15)]|
GET /statistics/settings/status||[**MonitoringStatus.get_statistics_settings**](vmngclient/endpoints/monitoring_status.py#L32)||DataSequence[[**Status**](vmngclient/endpoints/monitoring_status.py#L17)]|
GET /sdavc/cloudconnector||[**SDAVCCloudConnector.get_cloud_connector**](vmngclient/endpoints/sdavc_cloud_connector.py#L28)||[**CloudConnector**](vmngclient/endpoints/sdavc_cloud_connector.py#L10)|
GET /tenantbackup/list||[**TenantBackupRestore.list_tenant_backup**](vmngclient/endpoints/tenant_backup_restore.py#L35)||[**BackupFiles**](vmngclient/endpoints/tenant_backup_restore.py#L10)|
POST /tenant||[**TenantManagement.create_tenant**](vmngclient/endpoints/tenant_management.py#L118)|[**Tenant**](vmngclient/model/tenant.py#L21)|[**Tenant**](vmngclient/model/tenant.py#L21)|
POST /tenant/async||[**TenantManagement.create_tenant_async**](vmngclient/endpoints/tenant_management.py#L123)|[**Tenant**](vmngclient/model/tenant.py#L21)|[**TenantTaskId**](vmngclient/endpoints/tenant_management.py#L21)|
POST /tenant/bulk/async||[**TenantManagement.create_tenant_async_bulk**](vmngclient/endpoints/tenant_management.py#L128)|List[[**Tenant**](vmngclient/model/tenant.py#L21)]|[**TenantTaskId**](vmngclient/endpoints/tenant_management.py#L21)|
DELETE /tenant/{tenant_id}/delete||[**TenantManagement.delete_tenant**](vmngclient/endpoints/tenant_management.py#L134)|[**TenantDeleteRequest**](vmngclient/endpoints/tenant_management.py#L12)||
DELETE /tenant/bulk/async||[**TenantManagement.delete_tenant_async_bulk**](vmngclient/endpoints/tenant_management.py#L139)|[**TenantBulkDeleteRequest**](vmngclient/endpoints/tenant_management.py#L16)|[**TenantTaskId**](vmngclient/endpoints/tenant_management.py#L21)|
GET /tenantstatus||[**TenantManagement.get_all_tenant_statuses**](vmngclient/endpoints/tenant_management.py#L149)||DataSequence[[**TenantStatus**](vmngclient/endpoints/tenant_management.py#L54)]|
GET /tenant||[**TenantManagement.get_all_tenants**](vmngclient/endpoints/tenant_management.py#L154)||DataSequence[[**Tenant**](vmngclient/model/tenant.py#L21)]|
GET /tenant/{tenant_id}||[**TenantManagement.get_tenant**](vmngclient/endpoints/tenant_management.py#L159)||[**Tenant**](vmngclient/model/tenant.py#L21)|
GET /tenant/vsmart/capacity||[**TenantManagement.get_tenant_hosting_capacity_on_vsmarts**](vmngclient/endpoints/tenant_management.py#L164)||DataSequence[[**vSmartTenantCapacity**](vmngclient/endpoints/tenant_management.py#L103)]|
GET /tenant/vsmart||[**TenantManagement.get_tenant_vsmart_mapping**](vmngclient/endpoints/tenant_management.py#L169)||[**vSmartTenantMap**](vmngclient/endpoints/tenant_management.py#L109)|
PUT /tenant/{tenant_id}||[**TenantManagement.update_tenant**](vmngclient/endpoints/tenant_management.py#L182)|[**TenantUpdateRequest**](vmngclient/endpoints/tenant_management.py#L63)|[**Tenant**](vmngclient/model/tenant.py#L21)|
PUT /tenant/{tenant_id}/vsmart||[**TenantManagement.update_tenant_vsmart_placement**](vmngclient/endpoints/tenant_management.py#L187)|[**vSmartPlacementUpdateRequest**](vmngclient/endpoints/tenant_management.py#L98)||
POST /tenant/{tenant_id}/vsessionid||[**TenantManagement.vsession_id**](vmngclient/endpoints/tenant_management.py#L192)||[**vSessionId**](vmngclient/endpoints/tenant_management.py#L113)|
GET /tenantmigration/download/{path}||[**TenantMigration.download_tenant_data**](vmngclient/endpoints/tenant_migration.py#L39)||bytes|
POST /tenantmigration/export||[**TenantMigration.export_tenant_data**](vmngclient/endpoints/tenant_migration.py#L43)|[**Tenant**](vmngclient/model/tenant.py#L21)|[**ExportInfo**](vmngclient/endpoints/tenant_migration.py#L16)|
GET /tenantmigration/migrationToken||[**TenantMigration.get_migration_token**](vmngclient/endpoints/tenant_migration.py#L47)||str|
POST /tenantmigration/networkMigration||[**TenantMigration.migrate_network**](vmngclient/endpoints/tenant_migration.py#L56)|str|[**MigrationInfo**](vmngclient/endpoints/tenant_migration.py#L34)|
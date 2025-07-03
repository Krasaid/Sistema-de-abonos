# -- mode: python ; coding: utf-8 --
import os
from PyInstaller.utils.hooks import collect_submodules

a = Analysis(
    ['main.py'],
    pathex=['C:/Users/krasaid/Desktop/PAINFULLINK ABONOS'],
    binaries=[],
    datas=[('C:/Users/krasaid/AppData/Local/Programs/Python/Python313/Lib/site-packages/mysql/connector/plugins/mysql_native_password.py', 'mysql/connector/plugins')],
    hiddenimports=['mysql', 'mysql.connector', 'mysql.connector.1', 'mysql.connector.1.auth_client', 'mysql.connector.1.auth_staff', 'mysql.connector.1.db', 'mysql.connector.1.main', 'mysql.connector.1.screens_admin', 'mysql.connector.1.screens_client', 'mysql.connector.1.screens_manager', 'mysql.connector.1.screens_staff', 'mysql.connector._decorating', 'mysql.connector._scripting', 'mysql.connector.abstracts', 'mysql.connector.aio', 'mysql.connector.aio._decorating', 'mysql.connector.aio.abstracts', 'mysql.connector.aio.authentication', 'mysql.connector.aio.charsets', 'mysql.connector.aio.connection', 'mysql.connector.aio.cursor', 'mysql.connector.aio.logger', 'mysql.connector.aio.network', 'mysql.connector.aio.plugins', 'mysql.connector.aio.plugins.authentication_kerberos_client', 'mysql.connector.aio.plugins.authentication_ldap_sasl_client', 'mysql.connector.aio.plugins.authentication_oci_client', 'mysql.connector.aio.plugins.authentication_openid_connect_client', 'mysql.connector.aio.plugins.authentication_webauthn_client', 'mysql.connector.aio.plugins.caching_sha2_password', 'mysql.connector.aio.plugins.mysql_clear_password', 'mysql.connector.aio.plugins.mysql_native_password', 'mysql.connector.aio.plugins.sha256_password', 'mysql.connector.aio.protocol', 'mysql.connector.aio.utils', 'mysql.connector.authentication', 'mysql.connector.charsets', 'mysql.connector.connection', 'mysql.connector.connection_cext', 'mysql.connector.constants', 'mysql.connector.conversion', 'mysql.connector.cursor', 'mysql.connector.cursor_cext', 'mysql.connector.custom_types', 'mysql.connector.dbapi', 'mysql.connector.django', 'mysql.connector.django.base', 'mysql.connector.django.client', 'mysql.connector.django.compiler', 'mysql.connector.django.creation', 'mysql.connector.django.features', 'mysql.connector.django.introspection', 'mysql.connector.django.operations', 'mysql.connector.django.schema', 'mysql.connector.django.validation', 'mysql.connector.errorcode', 'mysql.connector.errors', 'mysql.connector.locales', 'mysql.connector.locales.eng', 'mysql.connector.locales.eng.client_error', 'mysql.connector.logger', 'mysql.connector.network', 'mysql.connector.opentelemetry', 'mysql.connector.opentelemetry.constants', 'mysql.connector.opentelemetry.context_propagation', 'mysql.connector.opentelemetry.instrumentation', 'mysql.connector.optionfiles', 'mysql.connector.plugins', 'mysql.connector.plugins.authentication_kerberos_client', 'mysql.connector.plugins.authentication_ldap_sasl_client', 'mysql.connector.plugins.authentication_oci_client', 'mysql.connector.plugins.authentication_openid_connect_client', 'mysql.connector.plugins.authentication_webauthn_client', 'mysql.connector.plugins.caching_sha2_password', 'mysql.connector.plugins.mysql_clear_password', 'mysql.connector.plugins.mysql_native_password', 'mysql.connector.plugins.sha256_password', 'mysql.connector.pooling', 'mysql.connector.protocol', 'mysql.connector.tls_ciphers', 'mysql.connector.types', 'mysql.connector.utils', 'mysql.connector.version'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)

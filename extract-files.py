#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2024 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixup_remove,
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)

namespace_imports = [
    'device/samsung/sm6150-common',
    'hardware/qcom-caf/sm8150',
    'hardware/qcom-caf/wlan',
    'hardware/samsung',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/commonsys/display',
    'vendor/qcom/opensource/commonsys-intf/display',
    'vendor/qcom/opensource/display',
]


def lib_fixup_vendor_suffix(lib: str, partition: str, *args, **kwargs):
    return f'{lib}_{partition}' if partition == 'vendor' else None


lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
    (
        'com.qualcomm.qti.ant@1.0',
        'vendor.qti.hardware.fm@1.0',
    ): lib_fixup_vendor_suffix,
    (
        'libwpa_client',
    ): lib_fixup_remove,
}

blob_fixups: blob_fixups_user_type = {
    ('vendor/lib64/libsec-ril.so', 'vendor/lib64/libsec-ril-dsds.so'): blob_fixup()
        .binary_regex_replace(b'ril.dds.call.slotid', b'vendor.calls.slotid')
        .sig_replace('60 0E 40 F9 82 0C 80 52 24 00 80 52 E1 03 15 AA E3 03 14 AA', '60 0E 40 F9 82 0C 80 52 24 00 80 52 E1 03 15 AA 03 00 80 D2'),
    ('vendor/lib64/hw/gatekeeper.mdfpp.so', 'vendor/lib64/libkeymaster_helper.so', 'vendor/lib64/libskeymaster4device.so'): blob_fixup()
        .replace_needed('libcrypto.so', 'libcrypto-v33.so'),
    ('vendor/lib/mediadrm/libwvdrmengine.so', 'vendor/lib/libwvhidl.so'): blob_fixup()
        .add_needed('libcrypto_shim.so'),
    ('vendor/etc/seccomp_policy/atfwd@2.0.policy'): blob_fixup()
        .add_line_if_missing('gettid: 1'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sm6150-common',
    'samsung',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()

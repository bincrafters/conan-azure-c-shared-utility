// Copyright (c) Microsoft. All rights reserved.
// Licensed under the MIT license. See LICENSE file in the project root for full license information.

#include <assert.h>
#include "azure_c_shared_utility/platform.h"


int main(int argc, char** argv)
{
    (void)argc, (void)argv;

    assert(platform_init() == 0);
    platform_deinit();

    return 0;
}

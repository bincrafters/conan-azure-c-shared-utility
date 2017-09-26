#include "azure_c_shared_utility/sastoken.h"

int main()
{
    STRING_HANDLE sas_token = SASToken_CreateString("key", "scope", "name", 987654321);
    return 0;
}

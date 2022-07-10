#include <openssl/evp.h>
#include <openssl/aes.h>

bool openssl_sm3_hash(const vector<string>& input,
    unsigned char* buffer,
    unsigned int* buf_len)
{
    if (input.empty())
        return false;

    memset(buffer, 0, *buf_len);

    EVP_MD_CTX* ctx = EVP_MD_CTX_new();

    // 设置使用SM3
    if (!EVP_DigestInit_ex(ctx, EVP_sm3(), NULL)) {
        cout << "Failed to init" << endl;
        return false;
    }

    for (const auto& i : input) {
        if (!EVP_DigestUpdate(ctx, i.c_str(), i.size())) {
            cout << "Failed to update" << endl;
            return false;
        }
    }

    if (!EVP_DigestFinal_ex(ctx, buffer, buf_len)) {
        cout << "Failed to final" << endl;
        return false;
    }

    EVP_MD_CTX_free(ctx);
    return true;
}

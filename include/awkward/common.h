// BSD 3-Clause License; see https://github.com/scikit-hep/awkward-1.0/blob/master/LICENSE

#ifndef AWKWARD_COMMON_H_
#define AWKWARD_COMMON_H_

#ifdef _MSC_VER
  #define EXPORT_SYMBOL __declspec(dllexport)
  #ifdef _WIN64
    typedef signed   __int64 ssize_t;
    typedef unsigned __int64 size_t;
  #else
    typedef signed   int     ssize_t;
    typedef unsigned int     size_t;
  #endif
  typedef   unsigned char    uint8_t;
  typedef   signed   char    int8_t;
  typedef   unsigned short   uint16_t;
  typedef   signed   short   int16_t;
  typedef   unsigned int     uint32_t;
  typedef   signed   int     int32_t;
  typedef   unsigned __int64 uint64_t;
  typedef   signed   __int64 int64_t;
  #define ERROR Error
#else
  #define EXPORT_SYMBOL __attribute__((visibility("default")))
  #include <cstddef>
  #include <cstdint>
  #define ERROR struct Error
#endif

#include <iostream>
#include <algorithm>
#include <map>
#include <vector>
#include <mutex>
#include <memory>
#include <cstring>

extern "C" {
  struct EXPORT_SYMBOL Error {
    const char* str;
    int64_t identity;
    int64_t attempt;
    bool pass_through;
  };

  const int8_t   kMaxInt8   =                 127;   // 2**7  - 1
  const uint8_t  kMaxUInt8  =                 255;   // 2**8  - 1
  const int32_t  kMaxInt32  =          2147483647;   // 2**31 - 1
  const uint32_t kMaxUInt32 =          4294967295;   // 2**32 - 1
  const int64_t  kMaxInt64  = 9223372036854775806;   // 2**63 - 2: see below
  const int64_t  kSliceNone = kMaxInt64 + 1;         // for Slice::none()

  inline struct Error
    success() {
        struct Error out;
        out.str = nullptr;
        out.identity = kSliceNone;
        out.attempt = kSliceNone;
        out.pass_through = false;
        return out;
    };

  inline struct Error
    failure(const char* str, int64_t identity, int64_t attempt, bool pass_through = false) {
        struct Error out;
        out.str = str;
        out.identity = identity;
        out.attempt = attempt;
        out.pass_through = pass_through;
        return out;
    };
}

#endif // AWKWARD_COMMON_H_

/*
 * This file exists because without #define MINIMP3_IMPLEMENTATION in some
 * file, the minimp3 symbols are never built, and I don't know how to define
 * a C macro in Cython
 */
#ifndef MINIMP3_IMPL_H
#define MINIMP3_IMPL_H
#define MINIMP3_IMPLEMENTATION

#include "minimp3.h"

#endif

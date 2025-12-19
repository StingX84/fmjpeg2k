/*
 *
 *  Copyright (C) 2015, Ing-Long Eric Kuo
 *  All rights reserved.  See COPYRIGHT file for details.
 *
 *  This software and supporting documentation were developed by
 *
 *
 *
 *  Module:  fmjpeg2k
 *
 *  Author:  Ing-Long Eric Kuo
 *
 *  Purpose: Contains preprocessor definitions
 *
 */


#ifndef DL2KDEFINE_H
#define DL2KDEFINE_H

#include "dcmtk/config/osconfig.h"

#include "dcmtk/ofstd/ofdefine.h"


#ifdef fmjpeg2k_SHARED
#  ifdef fmjpeg2k_EXPORTS /* BUILING library */
#    ifdef _WIN32
#      define FMJPEG2K_EXPORT __declspec(dllexport)
#    elif __GNUC__
#      define FMJPEG2K_EXPORT __attribute__ ((visibility("default")))
#    else
#      define FMJPEG2K_EXPORT
#    endif
#  else /* LINKING library */
#    ifdef _WIN32
#      define FMJPEG2K_EXPORT __declspec(dllimport)
#    else
#      define FMJPEG2K_EXPORT
#    endif
#  endif
#else
#  define FMJPEG2K_EXPORT
#endif


#endif

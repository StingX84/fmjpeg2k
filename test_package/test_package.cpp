#include "fmjpeg2k/djdecode.h"
#include "fmjpeg2k/djencode.h"

#include <iostream>

int main(int argc, char *argv[])
{
    FMJPEG2KDecoderRegistration::registerCodecs(EJ2KUC_never);
    FMJPEG2KEncoderRegistration::registerCodecs(false, 64, 64, true, 0, true, EJ2KUC_never, false);

    FMJPEG2KDecoderRegistration::cleanup();
    FMJPEG2KEncoderRegistration::cleanup();

    return 0;
}

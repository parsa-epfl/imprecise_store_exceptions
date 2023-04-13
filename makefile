AGFI ?= 09eae3473052a0cd3
BIN  ?= test.bin
IMG  ?= test.img
LOG  ?= test.log

MB   ?=

ARGS  = +rom=pre/rom.bin             \
        +bin=pre/$(BIN)              \
        +mm_readLatency_0=30         \
        +mm_readMaxReqs_0=8          \
        +mm_writeLatency_0=30        \
        +mm_writeMaxReqs_0=8         \
        +mm_relaxFunctionalModel_0=0 \
        +inc=50

ifeq ($(MB),)
ARGS += +img=pre/$(IMG)
endif


.PHONY: rst run


rst:
	@sudo fpga-load-local-image -S 0 -I agfi-$(AGFI) -H -F

run:
	@sudo stdbuf --output=L ./firesim $(ARGS) | tee post/$(LOG)


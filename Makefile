.PHONY: clean
all:make_python_lib smt2_to_maple random_NRA
## Load Previous Configuration ####################################################################

-include config.mk

## Configurable options ###########################################################################

# Directory to store object files, libraries, executables, and dependencies:
smtlib_parse_BUILD_DIR      ?= build
smtlib_parse_LIB_DIR   ?=lib
BIN_DIR ?= bin
# Include debug-symbols in release builds
smtlib_parse_RELSYM ?= -g

# Sets of compile flags for different build types
smtlib_parse_REL    ?= -O3 
smtlib_parse_DEB    ?=  -g -D DEBUG 
smtlib_parse_PRF    ?= -O3 -D NDEBUG
smtlib_parse_FPIC   ?= -fpic

# GNU Standard Install Prefix
smtlib_parse_prefix         ?= /usr/local

config:
	@( echo 'smtlib_parse_BUILD_DIR?=$(smtlib_parse_BUILD_DIR)'           ; \
	   echo 'smtlib_parse_LIB_DIR?=$(smtlib_parse_LIB_DIR)'           ; \
	   echo 'smtlib_parse_RELSYM?=$(smtlib_parse_RELSYM)' ; \
	   echo 'smtlib_parse_REL?=$(smtlib_parse_REL)'       ; \
	   echo 'smtlib_parse_DEB?=$(smtlib_parse_DEB)'       ; \
	   echo 'smtlib_parse_PRF?=$(smtlib_parse_PRF)'       ; \
	   echo 'smtlib_parse_FPIC?=$(smtlib_parse_FPIC)'     ; \
	   echo 'smtlib_parse_prefix?=$(smtlib_parse_prefix)'                 ) > config.mk

smtlib_parse_hh=$(wildcard src/*.hh)
CXX=g++ 
IPATHS=-ICLPoly/ -I./src
# --- 如果在 conda 环境下，优先用 conda 里的 Python include ---
ifdef CONDA_PREFIX
Ipython = -I$(CONDA_PREFIX)/include/python$(shell python3 -c "import sys;print(f'{sys.version_info[0]}.{sys.version_info[1]}')")
else
Ipython = -I/usr/include/python3.10
endif
CFLAGS=-O3 -flto 

clpolylib= -LCLPoly/lib/clpoly  -lclpoly -lgmpxx -lgmp

# --- Python 3.x 的 Boost.Python 库名通常是 boost_python3x ---	
PY_ABI := $(shell python3 -c "import sys;print(f'{sys.version_info[0]}{sys.version_info[1]}')")
pythonlib = -lboost_python$(PY_ABI)

smtlib_parse_hh=$(wildcard src/*.hh)
smtlib_parse_cc_=$(wildcard src/*.cc)
main_cc=src/smt2_to_maple.cc src/random_NRA.cc src/chordofsmt.cc
smtlib_parse_cc=$(filter-out $(main_cc),$(smtlib_parse_cc_))
smtlib_parse_d_o=$(smtlib_parse_cc:src/%.cc=$(smtlib_parse_BUILD_DIR)/debug/smtlib_parse/%.o)
smtlib_parse_r_o=$(smtlib_parse_cc:src/%.cc=$(smtlib_parse_BUILD_DIR)/release/smtlib_parse/%.o)
$(smtlib_parse_BUILD_DIR)/release/smtlib_parse/%.o:src/%.cc $(smtlib_parse_hh)
	mkdir -p $(smtlib_parse_BUILD_DIR)/release/smtlib_parse
	$(CXX) $(smtlib_parse_REL) $(smtlib_parse_FPIC) $(IPATHS) -c $< -o $@ $(clpolylib)
$(smtlib_parse_BUILD_DIR)/debug/%.o:%.cc $(smtlib_parse_hh)
	mkdir -p $(smtlib_parse_BUILD_DIR)/debug/smtlib_parse
	$(CXX) $(smtlib_parse_DEB) $(smtlib_parse_FPIC) $(IPATHS) -c $< -o $@ $(clpolylib)

# --- 若已激活 conda 环境：自动使用 conda 的 include/lib，并写入 rpath 便于运行时找库 ---
ifdef CONDA_PREFIX
IPATHS  += -I$(CONDA_PREFIX)/include
LDFLAGS += -L$(CONDA_PREFIX)/lib -Wl,-rpath,$(CONDA_PREFIX)/lib
endif

$(smtlib_parse_LIB_DIR)/smtlib_parse/NRA_op.so:$(smtlib_parse_r_o) python/NRA_op.cc
	mkdir -p $(dir $@)
	$(CXX) $(smtlib_parse_REL) $(smtlib_parse_FPIC) $(IPATHS) $(Ipython) $(smtlib_parse_r_o) python/NRA_op.cc -shared -o  $@ $(LDFLAGS) $(clpolylib) $(pythonlib)
make_python_lib:$(smtlib_parse_LIB_DIR)/smtlib_parse/NRA_op.so
smt2_to_maple:$(smtlib_parse_r_o)  src/smt2_to_maple.cc
	mkdir -p $(BIN_DIR)
	$(CXX) $(smtlib_parse_REL) $(smtlib_parse_FPIC) $(IPATHS) $(smtlib_parse_r_o) src/$@.cc -o  $(BIN_DIR)/$@  $(LDFLAGS) $(clpolylib)
chordofsmt:$(smtlib_parse_r_o)  src/chordofsmt.cc
	mkdir -p $(BIN_DIR)
	$(CXX) $(smtlib_parse_REL) $(smtlib_parse_FPIC) $(IPATHS) $(smtlib_parse_r_o) src/$@.cc -o  $(BIN_DIR)/$@  $(LDFLAGS) $(clpolylib)

random_NRA:$(smtlib_parse_r_o)  src/random_NRA.cc
	mkdir -p $(BIN_DIR)
	$(CXX) $(smtlib_parse_REL) $(smtlib_parse_FPIC) $(IPATHS) $(smtlib_parse_r_o) src/$@.cc -o  $(BIN_DIR)/$@  $(LDFLAGS) $(clpolylib) 

parsertest:$(smtlib_parse_r_o)  test/parsertest.cc
	mkdir -p $(BIN_DIR)
	$(CXX) $(smtlib_parse_REL) $(smtlib_parse_FPIC) $(IPATHS) $(smtlib_parse_r_o) test/$@.cc -o  $(BIN_DIR)/$@  $(LDFLAGS) $(clpolylib)

clean:
	rm -rf $(smtlib_parse_d_o) $(smtlib_parse_r_o) $(smtlib_parse_LIB_DIR)/smtlib_parse/NRA_op.so $(BIN_DIR)/*
#include "smtlib.hh"
#include "nra_analyze.hh"
#include <algorithm>
#include <filesystem>
#include <time.h>

int main(int argc, char const *argv[])
{
    std::string file_name="../smalltest=>.smt2";
    bool is_rename=true;

    auto lib=smt::smtlib::read_smtlib2(file_name,is_rename);
    std::cout<<lib<<std::endl;
    auto cnf=smt::NRA::smtlib_to_cnf(lib);
    std::cout<<cnf<<std::endl;

    return 0;
}
#include "smtlib.hh"
#include "nra_analyze.hh"
#include <algorithm>
#include <filesystem>
#include <time.h>
#include <Python.h>
#include <boost/python.hpp>
#include <boost/python/suite/indexing/vector_indexing_suite.hpp>


using namespace smt;
using namespace smt::NRA;
using namespace smt::smtlib;



// using namespace ;

class NRA_op
{
    public:
        NRA_CNF __cnf;
        NRA_op(){}
        NRA_op(const std::string & file_name,bool is_rename=false){
            auto t1=clock();
            auto lib=smt::smtlib::read_smtlib2(file_name,is_rename);
            __cnf=smt::NRA::smtlib_to_cnf(lib);
            std::cout<<"NRA_CNF time="<<double(clock()-t1)/CLOCKS_PER_SEC<<"s\n"; 
                
        }
        std::string str(){
            std::stringstream ss;
            ss<< __cnf;
            return ss.str();
        }

        boost::python::list vars(){
            boost::python::list v;
            for (auto & i:__cnf.vars())
            {
                v.append(i.str());
            }
            return v;
        }
        double op(boost::python::list  v,double dl_B=0,double dl_a=0,double deq_B=0,double deq_a=0)
        {
            size_t vl=boost::python::len(v);
            std::map<clpoly::variable,double> mv;
            auto ptr=__cnf.vars().begin();
            auto vi=0;
            for(;ptr!=__cnf.vars().end() && vi!=vl;++ptr,++vi)
            {
                mv.insert({*ptr,boost::python::extract<double>(v[vi])});
                // std::cout<<"{"<<*ptr<<" "<<boost::python::extract<double>(v[vi])<<"} ";
            }
            // std::cout<<std::endl;
            for(;ptr!=__cnf.vars().end();++ptr)
            {
                mv.insert({*ptr,0});
            }
            
            return __cnf.assign(mv,dl_B,dl_a,deq_B,deq_a);
            
        }
        size_t len()
        {
            return __cnf.cnf().size();
        }
        size_t C_len(size_t i)
        {
            // if (i>=__cnf.cnf().size())
            // {
            //     throw std::invalid_argument("输入越界");
            // }
            return __cnf.cnf().at(i).size();
        }
        std::string get_atom_str(size_t i,size_t j)
        {
            auto atom=__cnf.cnf().at(i).at(j);
            std::stringstream ss;
            ss<<__cnf.polyz(atom.first)<<atom.second<<0;
            return ss.str();
        }
        
};

BOOST_PYTHON_MODULE(NRA_op) { 
    boost::python::class_<std::vector<std::string>>("stringlist")
        .def(boost::python::vector_indexing_suite<std::vector<std::string>>() );
    boost::python::class_<std::vector<double>>("doublelist")
        .def(boost::python::vector_indexing_suite<std::vector<double>>() );
    
    boost::python::class_<NRA_op>("NRA_op", "NRA_op")
        .def(boost::python::init<>())
        .def(boost::python::init<const std::string &>())
        .def(boost::python::init<const std::string &,bool>())
        .def("vars", &NRA_op::vars,"get vars list" )
        .def("str", &NRA_op::str,"get str" )
        .def("len", &NRA_op::len)
        .def("C_len", &NRA_op::C_len )
        .def("get_atom_str", &NRA_op::get_atom_str )
        .def("op",&NRA_op::op,
"assign(A && B)=assign(A)+assign(B);\nassign(A || B)=assign(A)*assign(B);\nassign(f>0)={\n    (assign(f)>dl_B)? 0 :(assign(f)-dl_B)^2+ dl_a;\n};\nassign(f==0)={\n    (assign(f)>deq_B)? (assign(f)-deq_B)^2+ deq_a\n        :(\n            (assign(f)<-deq_B)?(assign(f)+deq_B)^2+ deq_a:0\n        )\n};\nassign(f<0)={\n    (assign(f)<-dl_B)? 0 :(assign(f)+dl_B)^2+ dl_a;\n};");
        
}
// extern "C"{
//     NRA_CNF* new_NRA_CNF(char * file_name)
//     {
//         auto lib=smt::smtlib::read_smtlib2(std::string(file_name),false);
//         NRA_CNF* ans=new NRA_CNF;
//         *ans=smt::NRA::smtlib_to_cnf(lib);
//         return ans;
//     }
//     void delete_NRA_CNF(NRA_CNF* NRA)
//     {
//         delete NRA;
//     } 
//     double NRA_CNF_assign(NRA_CNF* NRA,double* X,size_t len)
//     {
//         std::map<clpoly::variable,double>  Xmap;

//     }
//     size_t NRA_CNF_VAR_SIZE()
//     {

//     }


// }



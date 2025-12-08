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
        boost::python::list polys(){
            boost::python::list poly;
            for (auto & i:__cnf.polys())
            {
                poly.append(i.str());
            }
            return poly;
        }
        // 返回多项式元数据：每个元素是 { "coeffs": [...], "terms": [[var1id, exp1], [var2id, exp2], ...] }
        boost::python::list polys_meta() {
            boost::python::list plist;

            // 先建立 variable -> id 的映射（按照 __cnf.vars() 的全局顺序）
            std::map<clpoly::variable, int> v2id;
            {
                int idx = 0;
                for (const auto& v : __cnf.vars()) {
                    v2id.emplace(v, idx++);
                }
            }
            
            for (auto &p : __cnf.polys()) {
                boost::python::list coeffs;
                boost::python::list monos;

                for (auto &term : p) {
                    // term: pair<Monomial, Coeff>
                    // term.second 是 mpz_class 或 mpq_class
                    coeffs.append(term.second.get_d());

                    // term.first 是 vector<pair<variable,int64_t>>
                    boost::python::list mono_list;
                    for (auto &var_exp : term.first) {
                        boost::python::list ve;
                        ve.append(v2id.find(var_exp.first)->second);
                        ve.append(var_exp.second);
                        mono_list.append(ve); 
                    }
                    monos.append(mono_list);
                }

                boost::python::dict pd;
                pd["coeffs"] = coeffs;
                pd["monos"] = monos;
                plist.append(pd);
            }

            return plist;
        }

        boost::python::list cnf(){
            boost::python::list cnf;
            for (auto & i:__cnf.cnf())
            {
                boost::python::list clause;
                for (auto & j:i)
                {
                    boost::python::list atom;
                    atom.append(j.first);
                    atom.append(j.second);
                    clause.append(atom);
                }
                cnf.append(clause);
            }
            return cnf;
        }
        // 生成适合 Torch 的紧凑 CNF 元数据：
        // 返回 dict:
        // {
        //   "num_vars": int,
        //   "num_polys": int,
        //   "num_clauses": int,
        //   "vars": List[str],          // 变量顺序
        //   "polys_meta": List[Dict],  // 多项式元数据
        //   "cnf": List[List[Tuple[int, int]]], // 每个
        // }
        boost::python::dict meta()
        {
            boost::python::dict meta;
            meta["num_vars"] = static_cast<int>(__cnf.vars().size());
            meta["num_polys"] = static_cast<int>(__cnf.polys().size());
            meta["num_clauses"] = static_cast<int>(__cnf.cnf().size());
            meta["vars"] = this->vars();
            meta["polys_meta"] = this->polys_meta();
            meta["cnf"] = this->cnf();
            return meta;
        }
        
        // 计算当前 CNF 中所有多项式在给定赋值下的值
        // 输入:  v 为变量取值列表，按 __cnf.vars() 的顺序
        // 输出:  Python list，长度为 __cnf.polys().size()
        boost::python::list polys_value(boost::python::list v)
        {
            // 先把 Python list 转成 std::map<variable,double>
            size_t vl = boost::python::len(v);
            std::map<clpoly::variable,double> mv;

            auto ptr = __cnf.vars().begin();
            size_t vi = 0;
            for (; ptr != __cnf.vars().end() && vi != vl; ++ptr, ++vi) {
                mv.insert({*ptr, boost::python::extract<double>(v[vi])});
            }
            // 剩余变量默认补 0
            for (; ptr != __cnf.vars().end(); ++ptr) {
                mv.insert({*ptr, 0.0});
            }

            // 逐个多项式求值
            boost::python::list res;
            for (auto &p : __cnf.polys()) {
                // 假设 p.assign(mv) 可以转成 double
                double val = assign_poly(mv,p);
                res.append(val);
            }
            return res;
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
        .def("polys", &NRA_op::polys,"get polys list" )
        .def("polys_meta", &NRA_op::polys_meta,"get polys meta" )
        .def("cnf", &NRA_op::cnf,"get cnf list" )
        .def("meta", &NRA_op::meta,"get meta dict" )
        .def("str", &NRA_op::str,"get str" )
        .def("len", &NRA_op::len)
        .def("C_len", &NRA_op::C_len )
        .def("get_atom_str", &NRA_op::get_atom_str )
        .def("polys_value",&NRA_op::polys_value, "get polys value" )
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



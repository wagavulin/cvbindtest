#include <ruby.h>

#define PRINT_FUNC() fprintf(stderr, "[%s]\n", __func__)
#define PRINT_CXXFUNC() fprintf(stderr, "[CXX %s]\n", __func__)

#include "autogen/rbopencv_include.hpp"
using namespace cv;
static VALUE mCV2;
#include "autogen/rbopencv_classdef.hpp"

extern "C" {
void Init_cv2(){
    PRINT_FUNC();
    mCV2 = rb_define_module("CV2");

    cFoo = rb_define_class_under(mCV2, "Foo", rb_cObject);
    rb_define_alloc_func(cFoo, wrap_Foo_alloc);
    rb_define_private_method(cFoo, "initialize", RUBY_METHOD_FUNC(wrap_Foo_init), 0);
}
}

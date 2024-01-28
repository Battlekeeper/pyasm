Module(
    body=[
        ImportFrom(module="std_lib", names=[alias(name="*")], level=0),
        FunctionDef(
            name="main",
            args=arguments(
                posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]
            ),
            body=[
                AnnAssign(
                    target=Name(id="avar", ctx=Store()),
                    annotation=Name(id="int", ctx=Load()),
                    value=Constant(value=23),
                    simple=1,
                ),
                AnnAssign(
                    target=Name(id="bvar", ctx=Store()),
                    annotation=Name(id="float", ctx=Load()),
                    value=Constant(value=5.0),
                    simple=1,
                ),
                AnnAssign(
                    target=Name(id="cvar", ctx=Store()),
                    annotation=Name(id="float", ctx=Load()),
                    value=BinOp(
                        left=Name(id="avar", ctx=Load()),
                        op=Add(),
                        right=Name(id="bvar", ctx=Load()),
                    ),
                    simple=1,
                ),
                Expr(
                    value=Call(
                        func=Name(id="print_newline", ctx=Load()), args=[], keywords=[]
                    )
                ),
                Expr(
                    value=Call(
                        func=Name(id="print_float", ctx=Load()),
                        args=[Name(id="cvar", ctx=Load())],
                        keywords=[],
                    )
                ),
                Expr(
                    value=Call(
                        func=Name(id="print_newline", ctx=Load()), args=[], keywords=[]
                    )
                ),
                AnnAssign(
                    target=Name(id="dvar", ctx=Store()),
                    annotation=Name(id="float", ctx=Load()),
                    value=BinOp(
                        left=Name(id="cvar", ctx=Load()),
                        op=Sub(),
                        right=Constant(value=1),
                    ),
                    simple=1,
                ),
                Expr(
                    value=Call(
                        func=Name(id="print_float", ctx=Load()),
                        args=[Name(id="dvar", ctx=Load())],
                        keywords=[],
                    )
                ),
                Expr(
                    value=Call(
                        func=Name(id="terminate", ctx=Load()), args=[], keywords=[]
                    )
                ),
            ],
            decorator_list=[],
        ),
    ],
    type_ignores=[],
)
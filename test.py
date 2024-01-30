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
                    annotation=Name(id="float", ctx=Load()),
                    value=Constant(value=7.0),
                    simple=1,
                ),
                AnnAssign(
                    target=Name(id="bvar", ctx=Store()),
                    annotation=Name(id="float", ctx=Load()),
                    value=Constant(value=2.0),
                    simple=1,
                ),
                AnnAssign(
                    target=Name(id="cvar", ctx=Store()),
                    annotation=Name(id="float", ctx=Load()),
                    value=BinOp(
                        left=Name(id="avar", ctx=Load()),
                        op=Div(),
                        right=Name(id="bvar", ctx=Load()),
                    ),
                    simple=1,
                ),
                AnnAssign(
                    target=Name(id="dvar", ctx=Store()),
                    annotation=Name(id="int", ctx=Load()),
                    value=Name(id="cvar", ctx=Load()),
                    simple=1,
                ),
                Expr(
                    value=Call(
                        func=Name(id="print_int", ctx=Load()),
                        args=[Name(id="dvar", ctx=Load())],
                        keywords=[],
                    )
                ),
                Expr(
                    value=Call(
                        func=Name(id="print_newline", ctx=Load()), args=[], keywords=[]
                    )
                ),
                If(
                    test=Compare(
                        left=Name(id="dvar", ctx=Load()),
                        ops=[Gt()],
                        comparators=[Constant(value=3)],
                    ),
                    body=[
                        AnnAssign(
                            target=Name(id="tst", ctx=Store()),
                            annotation=Name(id="float", ctx=Load()),
                            value=Constant(value=69.0),
                            simple=1,
                        ),
                        Expr(
                            value=Call(
                                func=Name(id="print_float", ctx=Load()),
                                args=[Name(id="tst", ctx=Load())],
                                keywords=[],
                            )
                        ),
                        Expr(
                            value=Call(
                                func=Name(id="print_newline", ctx=Load()),
                                args=[],
                                keywords=[],
                            )
                        ),
                    ],
                    orelse=[],
                ),
                Expr(
                    value=Call(
                        func=Name(id="print_float", ctx=Load()),
                        args=[Name(id="cvar", ctx=Load())],
                        keywords=[],
                    )
                ),
            ],
            decorator_list=[],
        ),
    ],
    type_ignores=[],
)

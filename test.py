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
                    target=Name(id="index", ctx=Store()),
                    annotation=Name(id="float", ctx=Load()),
                    value=Constant(value=1.0),
                    simple=1,
                ),
                AnnAssign(
                    target=Name(id="total", ctx=Store()),
                    annotation=Name(id="float", ctx=Load()),
                    value=Constant(value=1.0),
                    simple=1,
                ),
                While(
                    test=Compare(
                        left=Name(id="index", ctx=Load()),
                        ops=[LtE()],
                        comparators=[Constant(value=10.0)],
                    ),
                    body=[
                        AnnAssign(
                            target=Name(id="total", ctx=Store()),
                            annotation=Name(id="float", ctx=Load()),
                            value=BinOp(
                                left=Name(id="total", ctx=Load()),
                                op=Mult(),
                                right=Name(id="index", ctx=Load()),
                            ),
                            simple=1,
                        ),
                        Expr(
                            value=Call(
                                func=Name(id="print_float", ctx=Load()),
                                args=[Name(id="total", ctx=Load())],
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
                        AnnAssign(
                            target=Name(id="index", ctx=Store()),
                            annotation=Name(id="float", ctx=Load()),
                            value=BinOp(
                                left=Name(id="index", ctx=Load()),
                                op=Add(),
                                right=Constant(value=1.0),
                            ),
                            simple=1,
                        ),
                    ],
                    orelse=[],
                ),
                Expr(
                    value=Call(
                        func=Name(id="print_newline", ctx=Load()), args=[], keywords=[]
                    )
                ),
                Expr(
                    value=Call(
                        func=Name(id="print_newline", ctx=Load()), args=[], keywords=[]
                    )
                ),
                Expr(
                    value=Call(
                        func=Name(id="print_float", ctx=Load()),
                        args=[Name(id="total", ctx=Load())],
                        keywords=[],
                    )
                ),
            ],
            decorator_list=[],
        ),
    ],
    type_ignores=[],
)

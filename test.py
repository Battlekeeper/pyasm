Module(
    body=[
        ImportFrom(module="std_lib", names=[alias(name="*")], level=0),
        FunctionDef(
            name="factorial",
            args=arguments(
                posonlyargs=[],
                args=[arg(arg="n", annotation=Name(id="int", ctx=Load()))],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=[
                AnnAssign(
                    target=Name(id="index", ctx=Store()),
                    annotation=Name(id="int", ctx=Load()),
                    value=Constant(value=1),
                    simple=1,
                ),
                AnnAssign(
                    target=Name(id="total", ctx=Store()),
                    annotation=Name(id="int", ctx=Load()),
                    value=Constant(value=1),
                    simple=1,
                ),
                While(
                    test=Compare(
                        left=Name(id="index", ctx=Load()),
                        ops=[LtE()],
                        comparators=[Name(id="n", ctx=Load())],
                    ),
                    body=[
                        AnnAssign(
                            target=Name(id="total", ctx=Store()),
                            annotation=Name(id="int", ctx=Load()),
                            value=BinOp(
                                left=Name(id="total", ctx=Load()),
                                op=Mult(),
                                right=Name(id="index", ctx=Load()),
                            ),
                            simple=1,
                        ),
                        Expr(
                            value=Call(
                                func=Name(id="print_int", ctx=Load()),
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
                            annotation=Name(id="int", ctx=Load()),
                            value=BinOp(
                                left=Constant(value=1),
                                op=Add(),
                                right=Name(id="index", ctx=Load()),
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
                        func=Name(id="print_int", ctx=Load()),
                        args=[Name(id="total", ctx=Load())],
                        keywords=[],
                    )
                ),
                Return(value=Name(id="total", ctx=Load())),
            ],
            decorator_list=[],
            returns=Name(id="int", ctx=Load()),
        ),
        FunctionDef(
            name="main",
            args=arguments(
                posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]
            ),
            body=[
                AnnAssign(
                    target=Name(id="n", ctx=Store()),
                    annotation=Name(id="int", ctx=Load()),
                    value=Constant(value=4),
                    simple=1,
                ),
                AnnAssign(
                    target=Name(id="r", ctx=Store()),
                    annotation=Name(id="int", ctx=Load()),
                    value=Call(
                        func=Name(id="factorial", ctx=Load()),
                        args=[Name(id="n", ctx=Load())],
                        keywords=[],
                    ),
                    simple=1,
                ),
                Expr(
                    value=Call(
                        func=Name(id="print_newline", ctx=Load()), args=[], keywords=[]
                    )
                ),
            ],
            decorator_list=[],
        ),
    ],
    type_ignores=[],
)

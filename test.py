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
                    target=Name(id="i", ctx=Store()),
                    annotation=Name(id="int", ctx=Load()),
                    value=Constant(value=0),
                    simple=1,
                ),
                While(
                    test=Compare(
                        left=Name(id="i", ctx=Load()),
                        ops=[Lt()],
                        comparators=[Constant(value=10)],
                    ),
                    body=[
                        Expr(
                            value=Call(
                                func=Name(id="print_int", ctx=Load()),
                                args=[Name(id="i", ctx=Load())],
                                keywords=[],
                            )
                        ),
                        AnnAssign(
                            target=Name(id="i", ctx=Store()),
                            annotation=Name(id="int", ctx=Load()),
                            value=BinOp(
                                left=Name(id="i", ctx=Load()),
                                op=Add(),
                                right=Constant(value=1),
                            ),
                            simple=1,
                        ),
                    ],
                    orelse=[],
                ),
                Expr(
                    value=Call(
                        func=Name(id="terminate", ctx=Load()), args=[], keywords=[]
                    )
                ),
            ],
            decorator_list=[],
            type_params=[],
        ),
    ],
    type_ignores=[],
)

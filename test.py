Module(
    body=[
        ImportFrom(module="std_lib", names=[alias(name="*")], level=0),
        FunctionDef(
            name="tst",
            args=arguments(
                posonlyargs=[],
                args=[arg(arg="arg1", annotation=Name(id="int", ctx=Load()))],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=[
                Return(
                    value=BinOp(
                        left=Constant(value=2),
                        op=Mult(),
                        right=Name(id="arg1", ctx=Load()),
                    )
                )
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
                    target=Name(id="i", ctx=Store()),
                    annotation=Name(id="int", ctx=Load()),
                    value=Constant(value=5),
                    simple=1,
                ),
                While(
                    test=Compare(
                        left=Name(id="i", ctx=Load()),
                        ops=[Gt()],
                        comparators=[Constant(value=0)],
                    ),
                    body=[
                        Expr(
                            value=Call(
                                func=Name(id="print_int", ctx=Load()),
                                args=[Name(id="i", ctx=Load()), Constant(value=1)],
                                keywords=[],
                            )
                        ),
                        AnnAssign(
                            target=Name(id="i", ctx=Store()),
                            annotation=Name(id="int", ctx=Load()),
                            value=BinOp(
                                left=Name(id="i", ctx=Load()),
                                op=Sub(),
                                right=Constant(value=1),
                            ),
                            simple=1,
                        ),
                    ],
                    orelse=[],
                ),
                Expr(
                    value=Call(
                        func=Name(id="print_int", ctx=Load()),
                        args=[Constant(value=0), Constant(value=1)],
                        keywords=[],
                    )
                ),
            ],
            decorator_list=[],
            returns=Name(id="void", ctx=Load()),
        ),
    ],
    type_ignores=[],
)

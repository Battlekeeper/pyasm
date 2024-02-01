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
                If(
                    test=Compare(
                        left=Name(id="n", ctx=Load()),
                        ops=[Eq()],
                        comparators=[Constant(value=0)],
                    ),
                    body=[Return(value=Constant(value=1))],
                    orelse=[
                        Return(
                            value=BinOp(
                                left=Name(id="n", ctx=Load()),
                                op=Mult(),
                                right=Call(
                                    func=Name(id="factorial", ctx=Load()),
                                    args=[
                                        BinOp(
                                            left=Name(id="n", ctx=Load()),
                                            op=Sub(),
                                            right=Constant(value=1),
                                        )
                                    ],
                                    keywords=[],
                                ),
                            )
                        )
                    ],
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
                    target=Name(id="result", ctx=Store()),
                    annotation=Name(id="int", ctx=Load()),
                    value=Call(
                        func=Name(id="factorial", ctx=Load()),
                        args=[Constant(value=5)],
                        keywords=[],
                    ),
                    simple=1,
                ),
                Expr(
                    value=Call(
                        func=Name(id="print_int", ctx=Load()),
                        args=[Name(id="result", ctx=Load()), Constant(value=1)],
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

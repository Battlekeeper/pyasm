Module(
    body=[
        ImportFrom(module="std_lib", names=[alias(name="*")], level=0),
        AnnAssign(
            target=Name(id="testvar", ctx=Store()),
            annotation=Name(id="float", ctx=Load()),
            value=Constant(value=69.0),
            simple=1,
        ),
        FunctionDef(
            name="factorial",
            args=arguments(
                posonlyargs=[],
                args=[arg(arg="n", annotation=Name(id="int", ctx=Load()))],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[Constant(value=420)],
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
            type_params=[],
        ),
        FunctionDef(
            name="main",
            args=arguments(
                posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]
            ),
            body=[
                Global(names=["testvar"]),
                Expr(
                    value=Call(
                        func=Name(id="print_int", ctx=Load()),
                        args=[
                            Call(
                                func=Name(id="factorial", ctx=Load()),
                                args=[Constant(value=5)],
                                keywords=[],
                            ),
                            Constant(value=1),
                        ],
                        keywords=[],
                    )
                ),
                Expr(
                    value=Call(
                        func=Name(id="print_float", ctx=Load()),
                        args=[Name(id="testvar", ctx=Load()), Constant(value=1)],
                        keywords=[],
                    )
                ),
            ],
            decorator_list=[],
            returns=Name(id="void", ctx=Load()),
            type_params=[],
        ),
    ],
    type_ignores=[],
)

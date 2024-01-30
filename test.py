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
                    value=Constant(value=0.0),
                    simple=1,
                ),
                While(
                    test=Compare(
                        left=Name(id="avar", ctx=Load()),
                        ops=[Lt()],
                        comparators=[Constant(value=10.0)],
                    ),
                    body=[
                        Expr(
                            value=Call(
                                func=Name(id="print_float", ctx=Load()),
                                args=[Name(id="avar", ctx=Load())],
                                keywords=[],
                            )
                        ),
                        Assign(
                            targets=[Name(id="avar", ctx=Store())],
                            value=BinOp(
                                left=Name(id="avar", ctx=Load()),
                                op=Add(),
                                right=Constant(value=1.0),
                            ),
                        ),
                    ],
                    orelse=[],
                ),
            ],
            decorator_list=[],
        ),
    ],
    type_ignores=[],
)

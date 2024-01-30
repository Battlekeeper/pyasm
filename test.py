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
                    value=Constant(value=7),
                    simple=1,
                ),
                AnnAssign(
                    target=Name(id="bvar", ctx=Store()),
                    annotation=Name(id="float", ctx=Load()),
                    value=Constant(value=2),
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
                If(
                    test=Compare(
                        left=Name(id="cvar", ctx=Load()),
                        ops=[Gt()],
                        comparators=[Name(id="cvar", ctx=Load())],
                    ),
                    body=[
                        Assign(
                            targets=[Name(id="tst", ctx=Store())],
                            value=Constant(value=69.0),
                        ),
                        Expr(
                            value=Call(
                                func=Name(id="print_float", ctx=Load()),
                                args=[Name(id="tst", ctx=Load())],
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
                Expr(
                    value=Call(
                        func=Name(id="print_newline", ctx=Load()), args=[], keywords=[]
                    )
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

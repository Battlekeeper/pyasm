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
                    orelse=[],
                ),
                If(
                    test=Compare(
                        left=Name(id="n", ctx=Load()),
                        ops=[NotEq()],
                        comparators=[Constant(value=0)],
                    ),
                    body=[
                        AnnAssign(
                            target=Name(id="next", ctx=Store()),
                            annotation=Name(id="int", ctx=Load()),
                            value=BinOp(
                                left=Name(id="n", ctx=Load()),
                                op=Sub(),
                                right=Constant(value=1),
                            ),
                            simple=1,
                        ),
                        AnnAssign(
                            target=Name(id="r", ctx=Store()),
                            annotation=Name(id="int", ctx=Load()),
                            value=Call(
                                func=Name(id="factorial", ctx=Load()),
                                args=[Name(id="next", ctx=Load())],
                                keywords=[],
                            ),
                            simple=1,
                        ),
                        AnnAssign(
                            target=Name(id="r", ctx=Store()),
                            annotation=Name(id="int", ctx=Load()),
                            value=BinOp(
                                left=Name(id="r", ctx=Load()),
                                op=Mult(),
                                right=Name(id="n", ctx=Load()),
                            ),
                            simple=1,
                        ),
                        Return(value=Name(id="r", ctx=Load())),
                    ],
                    orelse=[],
                ),
            ],
            decorator_list=[],
            returns=Name(id="int", ctx=Load()),
            type_params=[],
        ),
        FunctionDef(
            name="harmonic",
            args=arguments(
                posonlyargs=[],
                args=[arg(arg="n", annotation=Name(id="float", ctx=Load()))],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=[
                If(
                    test=Compare(
                        left=Name(id="n", ctx=Load()),
                        ops=[Lt()],
                        comparators=[Constant(value=2.0)],
                    ),
                    body=[Return(value=Constant(value=1.0))],
                    orelse=[],
                ),
                If(
                    test=Compare(
                        left=Name(id="n", ctx=Load()),
                        ops=[NotEq()],
                        comparators=[Constant(value=0.0)],
                    ),
                    body=[
                        AnnAssign(
                            target=Name(id="next", ctx=Store()),
                            annotation=Name(id="float", ctx=Load()),
                            value=BinOp(
                                left=Name(id="n", ctx=Load()),
                                op=Sub(),
                                right=Constant(value=1.0),
                            ),
                            simple=1,
                        ),
                        AnnAssign(
                            target=Name(id="r", ctx=Store()),
                            annotation=Name(id="float", ctx=Load()),
                            value=Call(
                                func=Name(id="harmonic", ctx=Load()),
                                args=[Name(id="next", ctx=Load())],
                                keywords=[],
                            ),
                            simple=1,
                        ),
                        AnnAssign(
                            target=Name(id="div", ctx=Store()),
                            annotation=Name(id="float", ctx=Load()),
                            value=BinOp(
                                left=Constant(value=1.0),
                                op=Div(),
                                right=Name(id="n", ctx=Load()),
                            ),
                            simple=1,
                        ),
                        AnnAssign(
                            target=Name(id="r", ctx=Store()),
                            annotation=Name(id="float", ctx=Load()),
                            value=BinOp(
                                left=Name(id="r", ctx=Load()),
                                op=Add(),
                                right=Name(id="div", ctx=Load()),
                            ),
                            simple=1,
                        ),
                        Return(value=Name(id="r", ctx=Load())),
                    ],
                    orelse=[],
                ),
            ],
            decorator_list=[],
            returns=Name(id="float", ctx=Load()),
            type_params=[],
        ),
        FunctionDef(
            name="main",
            args=arguments(
                posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]
            ),
            body=[
                AnnAssign(
                    target=Name(id="r", ctx=Store()),
                    annotation=Name(id="int", ctx=Load()),
                    value=Call(
                        func=Name(id="factorial", ctx=Load()),
                        args=[Constant(value=4)],
                        keywords=[],
                    ),
                    simple=1,
                ),
                Expr(
                    value=Call(
                        func=Name(id="print_int", ctx=Load()),
                        args=[Name(id="r", ctx=Load()), Constant(value=1)],
                        keywords=[],
                    )
                ),
                AnnAssign(
                    target=Name(id="h", ctx=Store()),
                    annotation=Name(id="float", ctx=Load()),
                    value=Call(
                        func=Name(id="harmonic", ctx=Load()),
                        args=[Constant(value=4.0)],
                        keywords=[],
                    ),
                    simple=1,
                ),
                Expr(
                    value=Call(
                        func=Name(id="print_float", ctx=Load()),
                        args=[Name(id="h", ctx=Load()), Constant(value=1)],
                        keywords=[],
                    )
                ),
            ],
            decorator_list=[],
            type_params=[],
        ),
    ],
    type_ignores=[],
)

Module(
    body=[
        AnnAssign(
            target=Name(id="new_line", ctx=Store()),
            annotation=Name(id="str", ctx=Load()),
            value=Constant(value="\\n"),
            simple=1,
        ),
        ClassDef(
            name="void",
            bases=[],
            keywords=[],
            body=[Pass()],
            decorator_list=[],
            type_params=[],
        ),
        FunctionDef(
            name="terminate",
            args=arguments(
                posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]
            ),
            body=[
                Expr(
                    value=Call(
                        func=Name(id="syscall", ctx=Load()),
                        args=[Constant(value=10)],
                        keywords=[],
                    )
                )
            ],
            decorator_list=[],
            returns=Name(id="void", ctx=Load()),
            type_params=[],
        ),
        FunctionDef(
            name="print_newline",
            args=arguments(
                posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]
            ),
            body=[
                Global(names=["new_line"]),
                Expr(
                    value=Call(
                        func=Name(id="syscall", ctx=Load()),
                        args=[Constant(value=4), Name(id="new_line", ctx=Load())],
                        keywords=[],
                    )
                ),
            ],
            decorator_list=[],
            returns=Name(id="void", ctx=Load()),
            type_params=[],
        ),
        FunctionDef(
            name="print_int",
            args=arguments(
                posonlyargs=[],
                args=[
                    arg(arg="number", annotation=Name(id="int", ctx=Load())),
                    arg(arg="new_line", annotation=Name(id="int", ctx=Load())),
                ],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=[
                Expr(
                    value=Call(
                        func=Name(id="syscall", ctx=Load()),
                        args=[Constant(value=1), Name(id="number", ctx=Load())],
                        keywords=[],
                    )
                ),
                If(
                    test=Compare(
                        left=Name(id="new_line", ctx=Load()),
                        ops=[Eq()],
                        comparators=[Constant(value=1)],
                    ),
                    body=[
                        Expr(
                            value=Call(
                                func=Name(id="print_newline", ctx=Load()),
                                args=[],
                                keywords=[],
                            )
                        )
                    ],
                    orelse=[],
                ),
            ],
            decorator_list=[],
            returns=Name(id="void", ctx=Load()),
            type_params=[],
        ),
        FunctionDef(
            name="print_float",
            args=arguments(
                posonlyargs=[],
                args=[
                    arg(arg="number", annotation=Name(id="float", ctx=Load())),
                    arg(arg="new_line", annotation=Name(id="int", ctx=Load())),
                ],
                kwonlyargs=[],
                kw_defaults=[],
                defaults=[],
            ),
            body=[
                Expr(
                    value=Call(
                        func=Name(id="syscall", ctx=Load()),
                        args=[Constant(value=2), Name(id="number", ctx=Load())],
                        keywords=[],
                    )
                ),
                If(
                    test=Compare(
                        left=Name(id="new_line", ctx=Load()),
                        ops=[Eq()],
                        comparators=[Constant(value=1)],
                    ),
                    body=[
                        Expr(
                            value=Call(
                                func=Name(id="print_newline", ctx=Load()),
                                args=[],
                                keywords=[],
                            )
                        )
                    ],
                    orelse=[],
                ),
            ],
            decorator_list=[],
            returns=Name(id="void", ctx=Load()),
            type_params=[],
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
                    value=Constant(value=1),
                    simple=1,
                ),
                While(
                    test=Compare(
                        left=Name(id="n", ctx=Load()),
                        ops=[NotEq()],
                        comparators=[Constant(value=1)],
                    ),
                    body=[
                        If(
                            test=Compare(
                                left=BinOp(
                                    left=Name(id="n", ctx=Load()),
                                    op=Mod(),
                                    right=Constant(value=2),
                                ),
                                ops=[Eq()],
                                comparators=[Constant(value=0)],
                            ),
                            body=[
                                AnnAssign(
                                    target=Name(id="n", ctx=Store()),
                                    annotation=Name(id="int", ctx=Load()),
                                    value=BinOp(
                                        left=Name(id="n", ctx=Load()),
                                        op=FloorDiv(),
                                        right=Constant(value=2),
                                    ),
                                    simple=1,
                                )
                            ],
                            orelse=[
                                AnnAssign(
                                    target=Name(id="n", ctx=Store()),
                                    annotation=Name(id="int", ctx=Load()),
                                    value=BinOp(
                                        left=BinOp(
                                            left=Constant(value=3),
                                            op=Mult(),
                                            right=Name(id="n", ctx=Load()),
                                        ),
                                        op=Add(),
                                        right=Constant(value=1),
                                    ),
                                    simple=1,
                                )
                            ],
                        )
                    ],
                    orelse=[],
                ),
            ],
            decorator_list=[],
            returns=Name(id="void", ctx=Load()),
            type_params=[],
        ),
    ],
    type_ignores=[],
)

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
                    target=Name(id="i", ctx=Store()),
                    annotation=Name(id="int", ctx=Load()),
                    value=Constant(value=10),
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
                        AugAssign(
                            target=Name(id="i", ctx=Store()),
                            op=Sub(),
                            value=Constant(value=1),
                        ),
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

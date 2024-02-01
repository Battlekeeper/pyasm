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
                    target=Name(id="a", ctx=Store()),
                    annotation=Name(id="int", ctx=Load()),
                    value=Constant(value=2),
                    simple=1,
                ),
                AnnAssign(
                    target=Name(id="b", ctx=Store()),
                    annotation=Name(id="int", ctx=Load()),
                    value=Constant(value=2),
                    simple=1,
                ),
                AnnAssign(
                    target=Name(id="c", ctx=Store()),
                    annotation=Name(id="int", ctx=Load()),
                    value=BinOp(
                        left=BinOp(
                            left=Name(id="a", ctx=Load()),
                            op=Mult(),
                            right=Constant(value=2),
                        ),
                        op=Add(),
                        right=BinOp(
                            left=Name(id="b", ctx=Load()),
                            op=Mult(),
                            right=Constant(value=2),
                        ),
                    ),
                    simple=1,
                ),
            ],
            decorator_list=[],
        ),
    ],
    type_ignores=[],
)

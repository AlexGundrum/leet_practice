importScripts('./pyodide.js');

let pyodideReady = false;
let pyodide = null;

async function load() {
    pyodide = await loadPyodide({ indexURL: './' });
    pyodideReady = true;
    postMessage({ type: 'ready' });
}

load().catch(err => {
    postMessage({ type: 'error', error: err.message });
});

onmessage = async (e) => {
    if (!pyodideReady) {
        postMessage({ type: 'run_error', id: e.data.id, error: 'Pyodide not ready yet.' });
        return;
    }

    const { id, code, testCases } = e.data;
    try {
        pyodide.globals.set("user_code", code);
        pyodide.globals.set("test_cases_json", testCases);
        const pyCode = `
import ast
import json
import traceback
from collections import defaultdict, deque, Counter
import heapq
import math
from typing import List, Optional, Dict, Tuple, Set

import sys, io

__out = io.StringIO()
__err = io.StringIO()
sys.stdout = __out
sys.stderr = __err

__global_scope = globals().copy()
__exec_error = None
__results = []

try:
    exec(user_code, __global_scope)
except Exception as e:
    __exec_error = traceback.format_exc()

if not __exec_error:
    tc_list = json.loads(test_cases_json)
    for tc in tc_list:
        try:
            call_str = tc["call"]
            code_ast = ast.parse(call_str)
            if code_ast.body and isinstance(code_ast.body[-1], ast.Expr):
                expr = code_ast.body[-1].value
                if len(code_ast.body) > 1:
                    exec(compile(ast.unparse(code_ast.body[:-1]), "<string>", "exec"), __global_scope)
                res = eval(compile(ast.unparse(expr), "<string>", "eval"), __global_scope)
            else:
                exec(compile(ast.unparse(code_ast.body), "<string>", "exec"), __global_scope)
                res = None

            passed = (str(res) == tc["expected"])
            __results.append({
                "pass": passed,
                "actual": str(res),
                "expected": tc["expected"],
                "error": None
            })
        except Exception as e:
            __results.append({
                "pass": False,
                "actual": None,
                "expected": tc["expected"],
                "error": traceback.format_exc()
            })

sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

json.dumps({
    "stdout": __out.getvalue(),
    "stderr": __err.getvalue(),
    "exec_error": __exec_error,
    "results": __results
})
`;
        const resultJson = await pyodide.runPythonAsync(pyCode);
        postMessage({ type: 'run_success', id, result: resultJson });
    } catch (err) {
        postMessage({ type: 'run_error', id, error: err.message });
    }
};

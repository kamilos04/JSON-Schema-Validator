import { useState, useRef } from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert"
import Editor from "@monaco-editor/react"

function safeJsonParse(text) {
  try {
    const parsed = JSON.parse(text)
    return { ok: true, value: parsed }
  } catch (e) {
    return { ok: false, message: e?.message ?? "Invalid JSON" }
  }
}

export default function App() {
  const [schema, setSchema] = useState("")
  const [data, setData] = useState("")
  const [errors, setErrors] = useState([])
  const [loading, setLoading] = useState(false)
  const [valid, setValid] = useState(null)
  const [apiError, setApiError] = useState("")

  const monacoRef = useRef(null)
  const editorRef = useRef(null)

  function handleEditorDidMount(editor, monaco) {
    editorRef.current = editor
    monacoRef.current = monaco
  }

  const handleFileDrop = (e, setter) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file && (file.type === "application/json" || file.name.endsWith(".json"))) {
      const reader = new FileReader()
      reader.onload = (event) => setter(event.target.result)
      reader.readAsText(file)
    }
  }

  const updateEditorMarkers = (validationErrors) => {
    if (!monacoRef.current || !editorRef.current) return
    const model = editorRef.current.getModel()
    if (!model) return

    const markers = validationErrors
      .filter((err) => typeof err.line === "number")
      .map((err) => ({
        startLineNumber: err.line,
        startColumn: 1,
        endLineNumber: err.line,
        endColumn: model.getLineMaxColumn(err.line),
        message: err.message,
        severity: monacoRef.current.MarkerSeverity.Error,
      }))

    monacoRef.current.editor.setModelMarkers(model, "json-validation", markers)
  }

  const handleValidate = async () => {
    setApiError("")
    setValid(null)
    const nextErrors = []

    if (!schema.trim()) nextErrors.push({ path: "schema", message: "Schema is empty" })
    if (!data.trim()) nextErrors.push({ path: "data", message: "Data is empty" })

    const sCheck = schema.trim() ? safeJsonParse(schema) : null
    const dCheck = data.trim() ? safeJsonParse(data) : null

    if (sCheck && !sCheck.ok) nextErrors.push({ path: "schema", message: sCheck.message })
    if (dCheck && !dCheck.ok) nextErrors.push({ path: "data", message: dCheck.message })

    if (nextErrors.length > 0) {
      setErrors(nextErrors)
      return
    }

    setLoading(true)
    setErrors([])

    try {
      const res = await fetch("/api/validate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ json: data, schema: schema }),
      })

      if (!res.ok) {
        const text = await res.text().catch(() => "")
        throw new Error(`HTTP ${res.status}. ${text}`)
      }

      const result = await res.json()
      setValid(!!result.valid)

      if (result.valid) {
        setErrors([])
        updateEditorMarkers([])
      } else {
        const apiErrors = Array.isArray(result.errors)
          ? result.errors.map((e) => ({
              path: e.path && e.path !== "#" ? e.path : "Root object",
              message: e.message ?? "Validation error",
              line: typeof e.line === "number" ? e.line + 1 : 1,
              isGlobal: typeof e.line !== "number"
            }))
          : [{ path: "System", message: "Unknown error", line: 1, isGlobal: true }]

        setErrors(apiErrors)
        updateEditorMarkers(apiErrors)
      }
    } catch (e) {
      setApiError(e?.message ?? "Network error")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-100 p-8 text-slate-900">
      <Card className="max-w-4xl mx-auto shadow-lg">
        <CardHeader className="border-b mb-4">
          <CardTitle>JSON Schema Validator</CardTitle>
        </CardHeader>

        <CardContent className="space-y-6">
          <div 
            className="space-y-2 group transition-all"
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => handleFileDrop(e, setSchema)}
          >
            <div className="flex justify-between items-center">
              <Label className="font-bold">JSON Schema</Label>
              <span className="text-[10px] uppercase text-slate-400 group-hover:text-blue-500 transition-colors">Drag & drop JSON file</span>
            </div>
            <div className="border rounded-md overflow-hidden focus-within:ring-2 ring-blue-500">
              <Editor
                height="200px"
                language="json"
                value={schema}
                onChange={(v) => setSchema(v ?? "")}
                options={{ minimap: { enabled: false }, scrollBeyondLastLine: false, automaticLayout: true }}
              />
            </div>
          </div>

          <div 
            className="space-y-2 group transition-all"
            onDragOver={(e) => e.preventDefault()}
            onDrop={(e) => handleFileDrop(e, setData)}
          >
            <div className="flex justify-between items-center">
              <Label className="font-bold">JSON Data</Label>
              <span className="text-[10px] uppercase text-slate-400 group-hover:text-blue-500 transition-colors">Drag & drop JSON file</span>
            </div>
            <div className="border rounded-md overflow-hidden focus-within:ring-2 ring-blue-500">
              <Editor
                height="250px"
                language="json"
                value={data}
                onMount={handleEditorDidMount}
                onChange={(v) => {
                  setData(v ?? "")
                  if (monacoRef.current && editorRef.current) {
                    monacoRef.current.editor.setModelMarkers(editorRef.current.getModel(), "json-validation", [])
                  }
                }}
                options={{ minimap: { enabled: false }, scrollBeyondLastLine: false, automaticLayout: true, glyphMargin: true }}
              />
            </div>
          </div>

          <Button className="w-full bg-slate-900 hover:bg-slate-800 text-white h-12" onClick={handleValidate} disabled={loading}>
            {loading ? "Validating..." : "Validate JSON"}
          </Button>

          {apiError && (
            <Alert variant="destructive">
              <AlertTitle>API Error</AlertTitle>
              <AlertDescription>{apiError}</AlertDescription>
            </Alert>
          )}

          {errors.length > 0 && (
            <Alert variant="destructive" className="animate-in fade-in slide-in-from-top-1">
              <AlertTitle>Validation Errors</AlertTitle>
              <AlertDescription>
                <ul className="list-disc pl-5 mt-2 space-y-1">
                  {errors.map((err, i) => (
                    <li key={i} className="text-sm">
                      <span className="font-mono font-bold bg-slate-100 px-1 rounded">{err.path}</span>: {err.message} 
                      <span className="text-slate-500 ml-2">(line {err.line})</span>
                    </li>
                  ))}
                </ul>
              </AlertDescription>
            </Alert>
          )}

          {valid === true && (
            <Alert className="bg-emerald-50 border-emerald-200 text-emerald-800 animate-in zoom-in-95">
              <AlertTitle className="font-bold">Success</AlertTitle>
              <AlertDescription>The JSON data is perfectly valid against the provided schema.</AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
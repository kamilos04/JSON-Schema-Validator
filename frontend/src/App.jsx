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
        body: JSON.stringify({
          json: data, 
          schema: schema,
        }),
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
              path: e.path ?? "",
              message: e.message ?? "Validation error",
              line: typeof e.line === "number" ? e.line + 1 : undefined,
            }))
          : [{ path: "", message: "Unknown validation error" }]

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
    <div className="min-h-screen bg-slate-100 p-8">
      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle>JSON Schema Validator</CardTitle>
        </CardHeader>

        <CardContent className="space-y-6">
          <div className="space-y-2">
            <Label>JSON Schema</Label>
            <Editor
              height="200px"
              language="json"
              value={schema}
              onChange={(v) => setSchema(v ?? "")}
              options={{ 
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                automaticLayout: true
              }}
            />
          </div>

          <div className="space-y-2">
            <Label>JSON Data</Label>
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
              options={{ 
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                automaticLayout: true,
                glyphMargin: true 
              }}
            />
          </div>

          <Button className="w-full" onClick={handleValidate} disabled={loading}>
            {loading ? "Validating..." : "Validate"}
          </Button>

          {apiError && (
            <Alert variant="destructive">
              <AlertTitle>API error</AlertTitle>
              <AlertDescription>{apiError}</AlertDescription>
            </Alert>
          )}

          {errors.length > 0 && (
            <Alert variant="destructive">
              <AlertTitle>Validation errors</AlertTitle>
              <AlertDescription>
                <ul className="list-disc pl-5">
                  {errors.map((err, i) => (
                    <li key={i}>
                      <strong>{err.path || "(root)"}</strong>: {err.message}
                      {typeof err.line === "number" ? ` (line: ${err.line})` : ""}
                    </li>
                  ))}
                </ul>
              </AlertDescription>
            </Alert>
          )}

          {valid === true && (
            <Alert className="bg-green-50 border-green-200">
              <AlertTitle className="text-green-800">OK</AlertTitle>
              <AlertDescription className="text-green-700">
                JSON is valid against schema.
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
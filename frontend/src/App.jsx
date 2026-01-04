import { useState } from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert"

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

  const handleValidate = async () => {
    setApiError("")
    setValid(null)

    const nextErrors = []

    if (!schema.trim()) nextErrors.push({ path: "schema", message: "Schema is empty" })
    if (!data.trim()) nextErrors.push({ path: "data", message: "Data is empty" })

    const s = schema.trim() ? safeJsonParse(schema) : null
    const d = data.trim() ? safeJsonParse(data) : null

    if (s && !s.ok) nextErrors.push({ path: "schema", message: s.message })
    if (d && !d.ok) nextErrors.push({ path: "data", message: d.message })

    if (nextErrors.length > 0) {
      setErrors(nextErrors)
      return
    }

    setLoading(true)
    setErrors([])

    try {
      const res = await fetch("api/validate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },

        body: JSON.stringify({
          json: JSON.stringify(d.value),
          schema: JSON.stringify(s.value),
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
      } else {
        const apiErrors = Array.isArray(result.errors)
          ? result.errors.map((e) => ({
              path: e.path ?? "",
              message: e.message ?? "Validation error",
              line: e.line,
            }))
          : [{ path: "", message: "Unknown validation error" }]

        setErrors(apiErrors)
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
            <Textarea
              rows={8}
              placeholder="Wklej JSON Schema..."
              value={schema}
              onChange={(e) => setSchema(e.target.value)}
            />
          </div>

          <div className="space-y-2">
            <Label>JSON Data</Label>
            <Textarea
              rows={8}
              placeholder="Wklej JSON do walidacji..."
              value={data}
              onChange={(e) => setData(e.target.value)}
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
            <Alert>
              <AlertTitle>OK</AlertTitle>
              <AlertDescription>JSON is valid against schema.</AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

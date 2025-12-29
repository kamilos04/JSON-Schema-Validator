import { useState } from "react"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert"

export default function App() {
  const [schema, setSchema] = useState("")
  const [data, setData] = useState("")
  const [errors, setErrors] = useState([])

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

          <Button
            className="w-full"
            onClick={() =>
              setErrors([
                { path: "/name", message: "should be string" },
                { path: "/age", message: "should be >= 18" },
              ])
            }
          >
            Validate
          </Button>

          {errors.length > 0 && (
            <Alert variant="destructive">
              <AlertTitle>Validation errors</AlertTitle>
              <AlertDescription>
                <ul className="list-disc pl-5">
                  {errors.map((err, i) => (
                    <li key={i}>
                      <strong>{err.path}</strong>: {err.message}
                    </li>
                  ))}
                </ul>
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

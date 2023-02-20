 curl --request POST \
  --url http://localhost:5001/push \
  --header 'content-type: application/json' \
  --data '{
  "device_id": "devID",
  "client_id": 115,
  "created_at": "2023-02-07 14:56:49.386042",
  "data": {
    "license_id": 21,
    "preds": [
      {
        "image_frame": 31,
        "prob": 0.25,
        "tags": [
          "temp"
        ]
      },
      {
        "image_frame": 32,
        "prob": 0.05,
        "tags": [
          "temp1"
        ]
      }
    ]
  }
}'


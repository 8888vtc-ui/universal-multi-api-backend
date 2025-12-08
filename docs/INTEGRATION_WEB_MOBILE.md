# 🌐 Intégration Web & Mobile - Universal Multi-API Backend

## ✅ Compatibilité

**OUI**, le backend est **100% compatible** avec :
- ✅ **Applications Web** (React, Vue, Next.js, Angular, etc.)
- ✅ **Applications Mobile** (React Native, Flutter, iOS, Android)
- ✅ **Desktop Apps** (Electron, Tauri, etc.)

---

## 🏗️ Architecture

Le backend est une **API REST** standard qui peut être consommée par n'importe quel client :

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Web App       │────▶│                  │◀────│  Mobile App     │
│  (React/Vue)    │     │  FastAPI Backend │     │ (React Native)  │
└─────────────────┘     │                  │     └─────────────────┘
                        │  REST API        │
┌─────────────────┐     │  + WebSocket     │     ┌─────────────────┐
│  Desktop App    │────▶│  + JWT Auth      │◀────│  iOS/Android    │
│  (Electron)     │     │  + CORS          │     │  Native         │
└─────────────────┘     └──────────────────┘     └─────────────────┘
```

---

## 🌐 Intégration Web

### Configuration CORS

Le backend est déjà configuré pour accepter les requêtes web :

```python
# backend/main.py
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Exemple React

```javascript
// services/api.js
const API_BASE_URL = 'http://localhost:8000/api';

class APIClient {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.token = localStorage.getItem('access_token');
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    return response.json();
  }

  // Authentification
  async register(email, username, password) {
    return this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ email, username, password }),
    });
  }

  async login(email, password) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await fetch(`${this.baseURL}/auth/login`, {
      method: 'POST',
      body: formData,
    });
    
    const data = await response.json();
    if (data.access_token) {
      localStorage.setItem('access_token', data.access_token);
      localStorage.setItem('refresh_token', data.refresh_token);
    }
    return data;
  }

  // Chat IA
  async chat(message) {
    return this.request('/chat', {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  }

  // Recherche universelle
  async search(query) {
    return this.request('/search/universal', {
      method: 'POST',
      body: JSON.stringify({ query }),
    });
  }

  // Vidéo IA
  async createVideo(text, avatarId = 'anna') {
    return this.request('/video/avatar/create', {
      method: 'POST',
      body: JSON.stringify({ text, avatar_id: avatarId }),
    });
  }
}

export default new APIClient();
```

### Exemple Vue.js

```vue
<template>
  <div>
    <input v-model="query" @keyup.enter="search" />
    <button @click="search">Rechercher</button>
    <div v-for="result in results" :key="result.id">
      {{ result.title }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      query: '',
      results: [],
    };
  },
  methods: {
    async search() {
      try {
        const response = await axios.post('http://localhost:8000/api/search/universal', {
          query: this.query,
        });
        this.results = response.data.results;
      } catch (error) {
        console.error('Erreur:', error);
      }
    },
  },
};
</script>
```

### Exemple Next.js

```typescript
// lib/api.ts
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export async function search(query: string) {
  const response = await fetch(`${API_URL}/search/universal`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query }),
  });
  
  return response.json();
}

// app/search/page.tsx
'use client';

import { useState } from 'react';
import { search } from '@/lib/api';

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  const handleSearch = async () => {
    const data = await search(query);
    setResults(data.results);
  };

  return (
    <div>
      <input
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
      />
      <button onClick={handleSearch}>Rechercher</button>
      {results.map((result) => (
        <div key={result.id}>{result.title}</div>
      ))}
    </div>
  );
}
```

---

## 📱 Intégration Mobile

### React Native

```javascript
// services/api.js
import AsyncStorage from '@react-native-async-storage/async-storage';

const API_BASE_URL = 'http://localhost:8000/api'; // Ou votre URL de production

class APIClient {
  async request(endpoint, options = {}) {
    const token = await AsyncStorage.getItem('access_token');
    const url = `${API_BASE_URL}${endpoint}`;
    
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error(`API Error: ${response.statusText}`);
    }

    return response.json();
  }

  async login(email, password) {
    const formData = new FormData();
    formData.append('username', email);
    formData.append('password', password);
    
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      body: formData,
    });
    
    const data = await response.json();
    if (data.access_token) {
      await AsyncStorage.setItem('access_token', data.access_token);
      await AsyncStorage.setItem('refresh_token', data.refresh_token);
    }
    return data;
  }

  async chat(message) {
    return this.request('/chat', {
      method: 'POST',
      body: JSON.stringify({ message }),
    });
  }
}

export default new APIClient();
```

### Flutter (Dart)

```dart
// lib/services/api_client.dart
import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';

class APIClient {
  static const String baseURL = 'http://localhost:8000/api';
  
  Future<Map<String, dynamic>> request(
    String endpoint, {
    String method = 'GET',
    Map<String, dynamic>? body,
  }) async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('access_token');
    
    final url = Uri.parse('$baseURL$endpoint');
    final headers = {
      'Content-Type': 'application/json',
      if (token != null) 'Authorization': 'Bearer $token',
    };
    
    http.Response response;
    if (method == 'GET') {
      response = await http.get(url, headers: headers);
    } else if (method == 'POST') {
      response = await http.post(
        url,
        headers: headers,
        body: body != null ? jsonEncode(body) : null,
      );
    } else {
      throw Exception('Method not supported');
    }
    
    if (response.statusCode >= 200 && response.statusCode < 300) {
      return jsonDecode(response.body);
    } else {
      throw Exception('API Error: ${response.statusCode}');
    }
  }
  
  Future<Map<String, dynamic>> login(String email, String password) async {
    final url = Uri.parse('$baseURL/auth/login');
    final response = await http.post(
      url,
      headers: {'Content-Type': 'application/x-www-form-urlencoded'},
      body: {
        'username': email,
        'password': password,
      },
    );
    
    final data = jsonDecode(response.body);
    if (data['access_token'] != null) {
      final prefs = await SharedPreferences.getInstance();
      await prefs.setString('access_token', data['access_token']);
      await prefs.setString('refresh_token', data['refresh_token']);
    }
    return data;
  }
  
  Future<Map<String, dynamic>> chat(String message) async {
    return request('/chat', method: 'POST', body: {'message': message});
  }
}
```

### iOS (Swift)

```swift
// APIClient.swift
import Foundation

class APIClient {
    static let shared = APIClient()
    private let baseURL = "http://localhost:8000/api"
    private var accessToken: String? {
        get { UserDefaults.standard.string(forKey: "access_token") }
        set { UserDefaults.standard.set(newValue, forKey: "access_token") }
    }
    
    func request(endpoint: String, method: String = "GET", body: [String: Any]? = nil) async throws -> [String: Any] {
        guard let url = URL(string: "\(baseURL)\(endpoint)") else {
            throw NSError(domain: "Invalid URL", code: 0)
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = method
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        if let token = accessToken {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }
        
        if let body = body {
            request.httpBody = try JSONSerialization.data(withJSONObject: body)
        }
        
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              httpResponse.statusCode == 200 else {
            throw NSError(domain: "API Error", code: 0)
        }
        
        return try JSONSerialization.jsonObject(with: data) as! [String: Any]
    }
    
    func login(email: String, password: String) async throws -> [String: Any] {
        guard let url = URL(string: "\(baseURL)/auth/login") else {
            throw NSError(domain: "Invalid URL", code: 0)
        }
        
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/x-www-form-urlencoded", forHTTPHeaderField: "Content-Type")
        
        let body = "username=\(email)&password=\(password)"
        request.httpBody = body.data(using: .utf8)
        
        let (data, _) = try await URLSession.shared.data(for: request)
        let result = try JSONSerialization.jsonObject(with: data) as! [String: Any]
        
        if let token = result["access_token"] as? String {
            accessToken = token
        }
        
        return result
    }
    
    func chat(message: String) async throws -> [String: Any] {
        return try await request(endpoint: "/chat", method: "POST", body: ["message": message])
    }
}
```

### Android (Kotlin)

```kotlin
// APIClient.kt
import android.content.Context
import android.content.SharedPreferences
import com.google.gson.Gson
import okhttp3.*
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.RequestBody.Companion.toRequestBody
import org.json.JSONObject
import java.io.IOException

class APIClient(private val context: Context) {
    private val baseURL = "http://localhost:8000/api"
    private val client = OkHttpClient()
    private val gson = Gson()
    private val prefs: SharedPreferences = context.getSharedPreferences("app_prefs", Context.MODE_PRIVATE)
    
    private fun getToken(): String? = prefs.getString("access_token", null)
    
    fun request(
        endpoint: String,
        method: String = "GET",
        body: JSONObject? = null
    ): String {
        val url = "$baseURL$endpoint"
        val requestBuilder = Request.Builder().url(url)
        
        // Headers
        requestBuilder.addHeader("Content-Type", "application/json")
        getToken()?.let {
            requestBuilder.addHeader("Authorization", "Bearer $it")
        }
        
        // Body
        if (body != null && method != "GET") {
            val requestBody = body.toString().toRequestBody("application/json".toMediaType())
            when (method) {
                "POST" -> requestBuilder.post(requestBody)
                "PUT" -> requestBuilder.put(requestBody)
                "DELETE" -> requestBuilder.delete(requestBody)
            }
        }
        
        val request = requestBuilder.build()
        val response = client.newCall(request).execute()
        
        if (!response.isSuccessful) {
            throw IOException("API Error: ${response.code}")
        }
        
        return response.body?.string() ?: ""
    }
    
    fun login(email: String, password: String): JSONObject {
        val url = "$baseURL/auth/login"
        val formBody = FormBody.Builder()
            .add("username", email)
            .add("password", password)
            .build()
        
        val request = Request.Builder()
            .url(url)
            .post(formBody)
            .build()
        
        val response = client.newCall(request).execute()
        val json = JSONObject(response.body?.string() ?: "{}")
        
        json.optString("access_token")?.let {
            prefs.edit().putString("access_token", it).apply()
        }
        
        return json
    }
    
    fun chat(message: String): JSONObject {
        val body = JSONObject().apply {
            put("message", message)
        }
        return JSONObject(request("/chat", "POST", body))
    }
}
```

---

## 🔐 Authentification

### Flow d'authentification

1. **Inscription** : `POST /api/auth/register`
2. **Connexion** : `POST /api/auth/login` → Reçoit `access_token` et `refresh_token`
3. **Requêtes protégées** : Header `Authorization: Bearer <access_token>`
4. **Refresh token** : `POST /api/auth/refresh` quand access token expire

### Stockage des tokens

- **Web** : `localStorage` ou `sessionStorage`
- **Mobile** : `AsyncStorage` (React Native), `SharedPreferences` (Android), `UserDefaults` (iOS)
- **Sécurité** : Ne jamais stocker en clair, utiliser Keychain/Keystore pour mobile

---

## 📡 Endpoints Principaux

### IA & Chat
- `POST /api/chat` - Chat avec IA
- `POST /api/embeddings` - Générer embeddings

### Recherche
- `POST /api/search/universal` - Recherche universelle
- `GET /api/search/quick?q=...` - Recherche rapide

### Vidéo IA
- `POST /api/video/avatar/create` - Créer vidéo avatar
- `GET /api/video/status/{video_id}` - Statut vidéo

### Assistant
- `POST /api/assistant/chat` - Chat avec assistant
- `GET /api/assistant/recommendations` - Recommandations

### Analytics
- `GET /api/analytics/metrics` - Métriques
- `GET /api/analytics/dashboard` - Dashboard

---

## ⚙️ Configuration

### Variables d'environnement

```env
# Backend
CORS_ORIGINS=http://localhost:3000,http://localhost:8080,https://yourdomain.com
JWT_SECRET_KEY=your-secret-key

# Frontend (exemple)
NEXT_PUBLIC_API_URL=http://localhost:8000/api
REACT_APP_API_URL=http://localhost:8000/api
```

### Production

Pour la production, configurez :
- **HTTPS** obligatoire
- **CORS** restreint aux domaines autorisés
- **Rate limiting** activé
- **JWT secret** fort et sécurisé

---

## 🚀 Déploiement

### Backend
- VPS, Cloud (AWS, GCP, Azure)
- Docker, Kubernetes
- Nginx reverse proxy

### Frontend Web
- Vercel, Netlify, Cloudflare Pages
- S3 + CloudFront
- VPS avec Nginx

### Mobile
- App Store (iOS)
- Google Play (Android)
- TestFlight / Internal Testing

---

## ✅ Checklist Intégration

### Web
- [ ] Configurer CORS dans backend
- [ ] Créer client API
- [ ] Implémenter authentification
- [ ] Gérer tokens (localStorage)
- [ ] Gérer erreurs et retry
- [ ] Tests E2E

### Mobile
- [ ] Configurer URL API (production)
- [ ] Créer client API
- [ ] Implémenter authentification
- [ ] Stocker tokens (Keychain/Keystore)
- [ ] Gérer offline/online
- [ ] Push notifications (optionnel)
- [ ] Tests sur devices

---

## 📚 Ressources

- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [React Native Networking](https://reactnative.dev/docs/network)
- [Flutter HTTP](https://docs.flutter.dev/cookbook/networking/fetch-data)
- [iOS URLSession](https://developer.apple.com/documentation/foundation/urlsession)
- [Android OkHttp](https://square.github.io/okhttp/)

---

**Conclusion** : Le backend est **100% compatible** avec web et mobile grâce à son architecture REST standard. Il suffit de créer un client API dans votre framework préféré !

**Dernière mise à jour** : Décembre 2024


<<<<<<< Updated upstream
=======





>>>>>>> Stashed changes

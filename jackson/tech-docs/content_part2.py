# -*- coding: utf-8 -*-
"""Page bodies: Service Layer, Domain Workflows, AI & Resume, Web, Mobile, Admin, Ops."""
from content_part1 import dia

IMG = "assets/img"

# ==========================================================================
SERVICES = ("services",
    "Service Layer",
    "Service Layer",
    "The business logic lives in Nullref.Locumfy.DataProvider.Services.Core — a feature-sliced set of "
    "scoped services registered by convention, guarded by a recursive validation engine, and fed by "
    "request-scoped resolver caches.",
    f"""
<h2 id="slices">Feature slices</h2>
<p>Services are organized under <code>Features/&lt;Feature&gt;/{{Services,Models,Utilities}}</code>.
Large services are split into <code>partial</code> class files by concern.</p>
<div class="table-wrap"><table>
<thead><tr><th>Feature</th><th>Key service(s)</th><th>Responsibility</th></tr></thead>
<tbody>
<tr><td>Candidate</td><td><code>CandidateService</code> (partials: <code>.Candidate</code>, <code>.Jobs</code>, <code>.Network</code>, <code>.Timesheets</code>, <code>.Applications</code>, <code>.Documents</code>, <code>.Npi</code>, <code>.Resume</code>, <code>.AiSummary</code>, <code>.ProfilePdf</code>, <code>.W9</code>), <code>CandidateProfileService</code>, <code>CandidateSubscriptionService</code></td><td>The entire candidate surface: account, ~16 profile sub-resources, jobs, network, documents, AI summary, exports</td></tr>
<tr><td>Employer</td><td><code>EmployerService</code> (partials: <code>.cs</code>, <code>.Jobs</code>, <code>.Applications</code>, <code>.Candidates</code>, <code>.Network</code>, <code>.Timesheets</code>, <code>.Agreement</code>)</td><td>Company/account, job posting, application workflow, candidate search &amp; standardized resume</td></tr>
<tr><td>SecurityToken</td><td><code>TokenService</code></td><td>Issues/validates self-generated JWTs; role constants</td></tr>
<tr><td>Login</td><td><code>LoginService</code></td><td>Credential check (candidate then employer) &rarr; token</td></tr>
<tr><td>Messaging</td><td><code>MessagingService</code></td><td>Thread-based chat across candidate &amp; employer identities</td></tr>
<tr><td>Timesheet</td><td><code>TimesheetService</code></td><td>Shared timesheet logic + HTML/PDF rendering</td></tr>
<tr><td>AiGeneration</td><td><code>AiGenerationService</code></td><td>Pluggable LLM client (cloud or local/open-source)</td></tr>
<tr><td>Feed / News / Document / StaticData</td><td><code>FeedService</code>, <code>NewsService</code>, <code>DocumentService</code>, <code>StaticDataService</code></td><td>Activity feed, news, S3-backed documents, lookup data</td></tr>
</tbody></table></div>

<h2 id="di">Dependency injection &amp; base classes</h2>
<p>Services are marked <code>[ScopedLifetime]</code> and auto-registered by a Scrutor assembly scan
(<code>InstallServicesAllAssemblies</code>). To keep constructors small, an
<code>IServiceConfiguration</code> aggregate is injected into every service, bundling the
<code>DataContext</code>, logging, the <code>IUserContextService</code>, and the three resolvers.</p>
<pre><code><span class="tok-c">// ServiceBase : DatabaseService : LoggerContainer</span>
<span class="tok-k">public class</span> <span class="tok-t">CandidateService</span> : <span class="tok-t">ServiceBase</span>, <span class="tok-t">ICandidateService</span>
{{
    <span class="tok-c">// _context, _userContextService, scoped logging inherited from ServiceBase</span>
}}</code></pre>

<h2 id="validation">The validation engine</h2>
<p>UI models returned by / accepted by the API implement <code>IModel</code> and derive from
<code>AbstractValidatableModel</code>. Services call <code>model.Validate()</code> explicitly. The engine
(<code>Infrastructure/ValidatableObjectExtensions.Validate&lt;T&gt;()</code>) does more than
<code>Validator.TryValidateObject</code>:</p>
<ul>
<li>Recursively walks object graphs and <code>List&lt;T&gt;</code> children.</li>
<li>Auto-trims <code>[AutoTrim]</code> strings and HTML-sanitizes string input.</li>
<li>Adds rules the attributes miss: non-nullable <code>[Required]</code> <code>DateTime</code>/<code>LocalDate</code> must not be default; <code>Guid</code> must not be <code>Guid.Empty</code>.</li>
<li>On failure throws <code>RequestValidationException</code> with a per-field error dictionary &rarr; HTTP 422.</li>
</ul>
<div class="callout note"><span class="h">Model rules</span>
Value-type non-nullable properties on UI models are <code>[Required]</code>; sortable fields use
<code>[Sortable]</code>; date ranges use <code>[LocalDateTimeRange]</code>. This keeps validation and
Swagger metadata declarative.</div>

<h2 id="resolvers">Resolvers (request-scoped caches)</h2>
<p>To avoid N+1 queries when mapping many rows, <code>ResolverBase&lt;TKey,TResult&gt;</code> provides
thread-safe, request-scoped <code>ConcurrentDictionary</code> caches that batch-load and memoize common
lookups: <code>CompanyResolver</code>, <code>JobApplicationResolver</code> (loads in chunks of 50,
<code>AsNoTracking</code>), <code>StateResolver</code>, <code>ProfessionResolver</code>.</p>

<h2 id="mapping">Entity &rarr; UI-model mapping</h2>
<p><code>CandidateProfileService.BuildProfile(candidateId, includePrivate)</code> is the canonical mapper:
it loads the candidate plus ~18 related collections and projects them into <code>Profile*ItemModel</code>
types, resolves state/profession/title display names, derives the active job from the single
<code>Facility_Accepted</code> application, and computes a <code>PercentComplete</code> score.
<code>EmployerService.Candidates.GetCandidate</code> produces the employer-facing view of the same
profile data.</p>
""")


# ==========================================================================
WORKFLOWS = ("workflows",
    "Domain Workflows",
    "Domain Workflows",
    "The two workflows that define the marketplace: the job-application state machine (which enforces "
    "one active job per candidate) and the timesheet lifecycle.",
    f"""
<h2 id="application">Job-application state machine</h2>
<p>An employer posts a <code>Job</code>. A candidate views it and applies, creating a
<code>JobApplication</code>. The application&rsquo;s state (<code>JobCompletedTypeConstants</code>) drives
everything from there.</p>
{dia("job_state_machine",
     "Application states and transitions. Rejected states are terminal and read-only.")}
<ol>
<li><strong>Apply</strong> &rarr; <code>Provider_Accepted</code>. The candidate&rsquo;s intent. A snapshot of
the job is zipped into <code>JobXml</code> at apply time. Applying is blocked while the candidate has any
<code>Facility_Accepted</code> application.</li>
<li><strong>Candidate cancels</strong> &rarr; <code>Provider_Rejected</code> &mdash; terminal, read-only.</li>
<li><strong>Employer accepts</strong> &rarr; <code>Facility_Accepted</code>. Side effects: every other
<code>Provider_Accepted</code> application for that candidate is set to rejected (one active job at a
time), and <code>Job.FilledJobApplicationId</code> is stamped.</li>
<li><strong>Employer rejects</strong> &rarr; <code>FacilityRejected</code> &mdash; terminal.</li>
<li><strong>Employer completes</strong> &rarr; <code>Complete</code>, closing the job.</li>
</ol>
<div class="callout note"><span class="h">Authorization</span>
Only the candidate who owns an application can accept/cancel it; only the employer whose company posted
the job can accept/reject/complete it. Employer-side actions are scoped by a <code>Job.CompanyId</code>
join to the caller&rsquo;s company.</div>

<h2 id="timesheet">Timesheet lifecycle</h2>
<p>Timesheets are the billing primitive. Only a candidate can create one, and only for a job whose
application is in <code>Facility_Accepted</code>. Only the posting employer can approve it.</p>
{dia("timesheet_lifecycle",
     "Timesheet states 1→5, with rejection from ProviderApproved. Rendered to HTML then PDF via PuppeteerSharp.")}
<div class="table-wrap"><table>
<thead><tr><th>State</th><th>Value</th><th>Set by</th></tr></thead>
<tbody>
<tr><td><code>Open</code></td><td>1</td><td>Candidate creates/edits the 7-day entry</td></tr>
<tr><td><code>ProviderApproved</code></td><td>2</td><td>Candidate submits</td></tr>
<tr><td><code>ClientApproved</code></td><td>3</td><td>Employer approves</td></tr>
<tr><td><code>Rejected</code></td><td>4</td><td>Employer rejects (from submitted)</td></tr>
<tr><td><code>Paid</code></td><td>5</td><td>Payment/settlement</td></tr>
</tbody></table></div>
<p>Both candidate and employer can render a timesheet to HTML or PDF
(<code>GET …/timesheet/{{id}}/html</code> · <code>/pdf</code>); the PDF is produced by
<code>TimesheetService</code> building HTML and handing it to <code>PdfGenerator</code> (PuppeteerSharp).</p>

<h2 id="resume-flow">Resume &amp; onboarding flows</h2>
<p>Two adjacent flows are covered in detail on the
<a href="ai-resume.html">AI &amp; Resume Engine</a> page:</p>
<ul>
<li><strong>Resume upload &rarr; auto-fill.</strong> <code>POST candidate/document/resume-upload</code> parses
the file and populates the candidate&rsquo;s profile sub-resources (only <em>auto-generated</em> rows are
replaced, never user-entered data).</li>
<li><strong>NPI onboarding.</strong> <code>POST candidate/create-account-npi</code> bootstraps an account
from an NPI registry lookup.</li>
<li><strong>Standardized / anonymized resume.</strong> Employers download a branded, optionally
anonymized resume via <code>GET employer/candidate/{{id}}/resume</code>.</li>
</ul>
""")


# ==========================================================================
AI = ("ai",
    "AI &amp; Resume Engine",
    "AI &amp; Resume Engine",
    "The subsystem that makes Locumfy more than a job board: it ingests raw resumes at scale, extracts "
    "structured candidate data, and produces standardized/anonymized resumes plus LLM-generated "
    "summaries and verification notes.",
    f"""
<h2 id="pipeline">End-to-end pipeline</h2>
{dia("resume_pipeline",
     "A raw resume is converted to text, parsed into a structured graph, persisted as candidate rows, then fanned out to four downstream artifacts.")}

<h2 id="projects">Projects involved</h2>
<div class="table-wrap"><table>
<thead><tr><th>Project</th><th>Role</th><th>Notable libraries</th></tr></thead>
<tbody>
<tr><td><code>Parsing.PdfUtils</code></td><td>Layout-aware PDF text extraction</td><td>UglyToad.PdfPig (Docstrum block analysis)</td></tr>
<tr><td><code>Parsing</code></td><td>The parsing engine (~19 section parsers, dictionaries, OCR fallback)</td><td>DocumentConversion, Sovren SRP (<code>SrpAllInOne.dll</code>, backstop)</td></tr>
<tr><td><code>ResumeParser</code></td><td>Maps the parsed graph onto EF Core candidate rows</td><td>&mdash;</td></tr>
<tr><td><code>Services.ResumeBuilder</code></td><td>Generates standardized/anonymized resume PDFs</td><td>PuppeteerSharp (HTML&rarr;PDF)</td></tr>
<tr><td><code>AiData</code></td><td>Builds the LLM prompt (Markdown dossier) from candidate data</td><td>EF Core</td></tr>
<tr><td><code>Services.Core/Features/AiGeneration</code></td><td>The production LLM client</td><td>IHttpClientFactory, IOptions</td></tr>
<tr><td><code>ResumeExportTraining</code></td><td>Console tool: exports (text &rarr; JSON) training pairs</td><td>EF Core</td></tr>
</tbody></table></div>

<h2 id="parse">Parsing &amp; structuring</h2>
<p>Entry point <code>ParsingDomain.GetResumeEntity(ParseParameter)</code> returns a
<code>ResumeStandardItem</code> &mdash; a serializable graph of contact info, licenses (NPI/DEA/FCVS/
Medicaid/visa), specialties, years of experience, and typed lists (work history, education, skills,
publications, and so on). The pipeline:</p>
<ol>
<li><strong>To text.</strong> PDFs via <code>PdfUtils.PdfTextExtractor</code> (PdfPig + Docstrum layout so
multi-column resumes linearize sensibly); Word/RTF/TXT via <code>DocumentConversion.DocumentConverter</code>.
Supported: <code>.doc .docx .rtf .txt .pdf</code>.</li>
<li><strong>OCR fallback.</strong> If a PDF yields no text and <code>AllowPdfOcr</code> is set, the file is
POSTed to an external OCR web service and re-extracted.</li>
<li><strong>Segment &amp; parse.</strong> A <code>DocumentAbstract</code> splits the resume into blocks; ~19
<code>Parse&lt;Section&gt;()</code> methods plus dictionary/regex license finders extract structured data.
Sovren SRP is now only a backstop for name fields.</li>
</ol>
<p><code>ResumeParser.ProcessResumePartial</code> then maps the graph onto <code>Candidate*</code> tables.
It is <strong>idempotent</strong>: it deletes only <em>AutoGenerated</em> rows before re-adding, and only
overwrites identity/contact fields when the DB value is empty &mdash; user-entered data is never clobbered.
It also maps specialties via an embedded alias map, detects advanced certs (ACLS/BLS/NRP/PALS), and
builds <code>CandidateSearchData</code> for search.</p>

<h2 id="standardized">Standardized &amp; anonymized resumes</h2>
<p><code>ResumeDomain.GetStandardResume(context, ResumeParam)</code> returns <code>byte[]?</code> (null when
the candidate is missing). <code>ResumeParam</code>: <code>CandidateId</code>, <code>Anonymized</code>,
<code>Teaser</code>, <code>Output</code> (<code>OutputFormatConstants.PDF | .Word</code>),
<code>CompiledBy</code> (company name shown on the doc), <code>LogoImage</code> (defaults to the Locumfy
logo). It loads the full candidate graph, optionally anonymizes (strips name/contact/employer, replaces
names with initials, hides details past the third item), builds HTML from embedded templates, and renders
it to PDF with PuppeteerSharp. PDF is the output format produced today (the <code>Output</code> enum also
defines a Word value).</p>

<h2 id="llm">LLM features</h2>
<div class="kv">
<dt>Prompt</dt><dd><code>AiData.CandidatePromptBuilder</code> renders a Markdown dossier of the candidate and prepends a recruiter-style system instruction. Returns null if there is too little data (&lt; 300 chars).</dd>
<dt>Client</dt><dd><code>AiGenerationService.Generate(prompt)</code> uses <code>IHttpClientFactory</code> + <code>IOptions&lt;AiGenerationOptions&gt;</code> (config section <code>AiGeneration</code>). If <code>Ollama.UseLocal</code> it calls a local Ollama chat endpoint; otherwise a configurable cloud LLM (OpenAI-compatible chat-completions) endpoint.</dd>
<dt>AI summary</dt><dd><code>CandidateService.AiSummary.GenerateSummary()</code> stores the result in <code>Candidate.AiSummary</code>; <code>AiSummaryScore</code> is simply the summary&rsquo;s character count (not a quality metric).</dd>
<dt>AI verification</dt><dd><code>ResumeParser.CandidateDomain.BuildResumeVerificationNotes</code> asks the model to verify each publication/presentation; results are stored (zipped JSON) in <code>CandidateAiVerification</code>.</dd>
</div>
<p>Two LLM callers exist: <code>Core.AiGenerationService</code> (DI-injected, used by web features) and
<code>ResumeParser.AiCompletionService</code> (static, used by the offline/verification path). Both target
the same cloud/local providers.</p>

<h2 id="training">Training-data export</h2>
<p><code>ResumeExportTraining</code> is a console app that closes the loop: for every candidate with parsed
text it writes <code>docs/{{id}}.txt</code> (raw resume text, the <em>input</em>) and
<code>json/{{id}}.json</code> (a full <code>CandidateProfileModel</code>, the <em>target label</em>) &mdash; a
supervised dataset to eventually improve extraction. It targets a SQL Server copy of the data.</p>
""")


# ==========================================================================
WEB = ("web",
    "Web Frontend",
    "Web Frontend",
    "Nullref.Locumfy.Website — a React 18 + Vite SPA for candidates and employers. No TypeScript, no "
    "state library, no CSS framework: Context + hooks + a single hand-written stylesheet.",
    f"""
<h2 id="stack">Stack &amp; structure</h2>
<div class="kv">
<dt>Framework</dt><dd>React 18.2 + react-dom, Vite 5.1, react-router-dom 6.14, react-markdown 10 (AI summaries / feed)</dd>
<dt>Testing</dt><dd>Vitest 4 + Testing Library (jsdom), config inside <code>vite.config.js</code></dd>
<dt>Styling</dt><dd>One hand-written <code>src/styles.css</code> (~69&nbsp;KB) with CSS custom properties; light/dark via a <code>data-theme</code> attribute</dd>
<dt>API target</dt><dd><code>VITE_API_URL</code> &rarr; <code>Nullref.Locumfy.WebsiteApi</code> (dev <code>:5236</code>)</dd>
</div>
<p>Under <code>src/</code>: <code>api.js</code> (REST client), <code>App.jsx</code> (router shell),
<code>ThemeContext.jsx</code>, <code>components/</code> (shared UI incl. the 27&nbsp;KB
<code>MessagingPanel</code>), <code>pages/public/</code> (marketing), <code>pages/candidate/</code>,
<code>pages/employer/</code>.</p>

<h2 id="api">API client (<code>src/api.js</code>)</h2>
<ul>
<li>JWT in <code>localStorage</code> (<code>locumfy_token</code>); user object in <code>locumfy_user</code>; session restored on load.</li>
<li>Verbs <code>get/getWithBody/post/put/del</code> route through <code>request()</code>, which attaches <code>Authorization: Bearer</code>, parses errors into <code>Error</code> objects with <code>.status</code>/<code>.data</code>, and invokes a registered handler on 401 (logout &rarr; redirect).</li>
<li><code>download(path, fallbackName)</code> fetches as a blob with the auth header (a plain <code>&lt;a href&gt;</code> can&rsquo;t send the JWT) and honors <code>Content-Disposition</code>; <code>upload()</code> does multipart.</li>
<li><code>tryGet</code>/<code>tryPost</code> return <code>{{ data, live }}</code> so pages can show an offline-demo notice instead of crashing.</li>
</ul>

<h2 id="routing">Routing &amp; roles</h2>
<p>Role gating is by <code>user.role</code> (<code>candidate</code> | <code>facility</code>).
<code>/profile/*</code> is the candidate dashboard (redirects facility users to <code>/employer</code>);
<code>/employer/*</code> is the employer dashboard; <code>/in/:candidateId</code> is a public read-only
profile. Each dashboard shell hosts its own nested routes.</p>

<h2 id="screens">Key screens</h2>
<h3>Candidate section</h3>
<div class="table-wrap"><table>
<thead><tr><th>Page</th><th>Purpose</th></tr></thead>
<tbody>
<tr><td><code>Profile.jsx</code></td><td>Dashboard shell + landing feed</td></tr>
<tr><td><code>Me.jsx</code> (~58&nbsp;KB)</td><td>Full editable profile: all resume sections, AI summary, PDF/HTML export</td></tr>
<tr><td><code>Jobs.jsx</code></td><td>Search / Saved / Applied tabs; apply/save; enforces one-active-job</td></tr>
<tr><td><code>MyNetwork.jsx</code></td><td>3 tabs: Connections / Invitations / Grow; Premium/Credentialed/NPI badges</td></tr>
<tr><td><code>Timesheets.jsx</code></td><td>Weekly/monthly list + 7-day editor; submit; PDF/HTML</td></tr>
<tr><td><code>Documents.jsx</code></td><td>Upload / download / delete credential documents</td></tr>
<tr><td><code>Messaging.jsx</code></td><td>Wraps the shared <code>MessagingPanel</code></td></tr>
</tbody></table></div>
<h3>Employer section</h3>
<div class="table-wrap"><table>
<thead><tr><th>Page</th><th>Purpose</th></tr></thead>
<tbody>
<tr><td><code>Candidates.jsx</code></td><td>Candidate search, AI Summary, standardized <strong>Resume download</strong></td></tr>
<tr><td><code>MyJobs.jsx</code></td><td>Job posting CRUD</td></tr>
<tr><td><code>Applications.jsx</code></td><td>Review applications; accept / reject / complete (drives the state machine)</td></tr>
<tr><td><code>Timesheets.jsx</code></td><td>Approve / reject candidate timesheets</td></tr>
</tbody></table></div>

<div class="shots">
  <figure><img src="{IMG}/w-facility-jobs.png" alt="Employer — job postings screen"><figcaption>Employer &rsaquo; My Jobs</figcaption></figure>
  <figure><img src="{IMG}/w-facility-candidates.png" alt="Employer — candidate search screen"><figcaption>Employer &rsaquo; Candidates (AI summary + resume)</figcaption></figure>
  <figure><img src="{IMG}/w-facility-applications.png" alt="Employer — applications screen"><figcaption>Employer &rsaquo; Applications</figcaption></figure>
  <figure><img src="{IMG}/w-facility-timesheets.png" alt="Employer — timesheets screen"><figcaption>Employer &rsaquo; Timesheets</figcaption></figure>
</div>
<p class="dgm-cap">Website employer screens (from the marketing captures).</p>

<div class="callout todo"><span class="h">Maintainer note</span>
Screenshots live in <code>assets/img/</code> (copied from <code>marketing/</code>). Refresh them when the
UI changes materially. The website and mobile app are meant to stay feature-aligned &mdash; see the
<a href="mobile-app.html">Mobile App</a> page.</div>
""")


# ==========================================================================
MOBILE = ("mobile",
    "Mobile App",
    "Mobile App",
    "Nullref.Locumfy.Mobile — a Flutter/Dart companion app that mirrors the website&rsquo;s candidate "
    "experience against the same REST contract.",
    f"""
<h2 id="stack">Stack &amp; structure</h2>
<div class="kv">
<dt>Platform</dt><dd>Flutter (Material), Dart <code>^3.11.5</code>; android/ios/windows targets present</dd>
<dt>Networking</dt><dd><code>http ^1.2.0</code></dd>
<dt>Local storage</dt><dd><code>shared_preferences</code> (dark-mode only), <code>path_provider</code> (downloads), <code>file_picker</code> (uploads)</dd>
<dt>State</dt><dd>Plain <code>StatefulWidget</code> + <code>setState</code>; theme via a <code>ChangeNotifier</code> singleton (<code>ThemeController</code>). No provider/bloc/riverpod.</dd>
<dt>API target</dt><dd><code>http://10.0.2.2:5236/api</code> on Android emulator, <code>localhost:5236</code> elsewhere</dd>
</div>
<p>Under <code>lib/</code>: <code>main.dart</code>, <code>theme.dart</code>,
<code>models/api_models.dart</code> (~52&nbsp;KB of DTOs with <code>fromJson</code>),
<code>services/api_service.dart</code> (~42&nbsp;KB REST client), <code>screens/</code>,
<code>widgets/</code> (incl. a 21&nbsp;KB <code>section_editor</code>), <code>utils/</code>.</p>

<h2 id="nav">Navigation &amp; API layer</h2>
<p>Imperative <code>Navigator</code>: <code>SplashScreen</code> &rarr; <code>LoginScreen</code> &rarr;
<code>MainScreen</code>, a <code>BottomNavigationBar</code> over an <code>IndexedStack</code> of six tabs:
<strong>Profile (feed)</strong>, <strong>My Network</strong>, <strong>Jobs</strong>,
<strong>Timesheets</strong>, <strong>Messaging</strong>, <strong>Me</strong>.</p>
<p><code>ApiService.instance</code> is a singleton with <code>_get/_post/_put/_delete</code> helpers, a 5&nbsp;s
timeout, and <code>Bearer</code> auth. It covers the full candidate <em>and</em> facility surface (jobs,
applications, profile section CRUD, AI summary, messaging, network, feed, timesheets, documents, lookups).</p>
<div class="callout note"><span class="h">Session handling</span>
The mobile app holds the token in memory for the session, so the splash screen routes to login on each
launch. (The website, by contrast, restores its session from <code>localStorage</code>.)</div>

<h2 id="screens">Screens</h2>
<div class="shots phones">
  <figure><img src="{IMG}/m-login.png" alt="Mobile login screen"><figcaption>Login</figcaption></figure>
  <figure><img src="{IMG}/m-feed.png" alt="Mobile profile feed"><figcaption>Profile feed</figcaption></figure>
  <figure><img src="{IMG}/m-jobs.png" alt="Mobile jobs screen"><figcaption>Jobs</figcaption></figure>
  <figure><img src="{IMG}/m-network-grow.png" alt="Mobile network Grow tab"><figcaption>Network &rsaquo; Grow</figcaption></figure>
  <figure><img src="{IMG}/m-messaging.png" alt="Mobile messaging screen"><figcaption>Messaging</figcaption></figure>
  <figure><img src="{IMG}/m-timesheets.png" alt="Mobile timesheets screen"><figcaption>Timesheets</figcaption></figure>
  <figure><img src="{IMG}/m-me.png" alt="Mobile Me profile screen"><figcaption>Me (editable profile)</figcaption></figure>
</div>

<div class="table-wrap"><table>
<thead><tr><th>Screen</th><th>Notes</th></tr></thead>
<tbody>
<tr><td><code>network_screen.dart</code></td><td>3-tab <code>TabController</code> (Connections / Invitations / Grow); NPI + Credentialed badges</td></tr>
<tr><td><code>timesheets_screen.dart</code> (~71&nbsp;KB)</td><td>The largest screen: weekly/monthly + 7-day editor</td></tr>
<tr><td><code>profile_screen.dart</code> (~51&nbsp;KB)</td><td>&ldquo;Me&rdquo; editable profile with section editors</td></tr>
<tr><td><code>messaging_screen.dart</code></td><td>Conversation list + thread chat</td></tr>
<tr><td><code>documents_screen.dart</code></td><td>Document list / upload / download</td></tr>
</tbody></table></div>

<h2 id="parity">Parity with the website</h2>
<p>Same endpoints, same camelCase JSON, same <code>Bearer</code> JWT. Both implement the 3-tab Network,
the NPI/Premium/Credentialed badges, create-account-via-NPI, AI summaries, profile &amp; timesheet
PDF/HTML downloads, and a persisted light/dark theme (web <code>ThemeContext</code> &harr; mobile
<code>ThemeController</code>). Divergences: session persistence (web yes, mobile no) and navigation style
(declarative router vs imperative <code>Navigator</code>).</p>
""")


# ==========================================================================
ADMIN = ("admin",
    "Admin &amp; Analytics",
    "Admin &amp; Analytics",
    "An internal executive/investor metrics dashboard (Nullref.Locumfy.Adminsite) over its own API "
    "(Nullref.Locumfy.AdminWebsiteApi + Services.AdminCore) that surfaces platform KPIs and growth, "
    "liquidity, revenue, and engagement analytics.",
    f"""
<h2 id="site">Admin site</h2>
<div class="kv">
<dt>Stack</dt><dd>React 18 + Vite 5 + react-router 6 (same toolchain as the website, leaner deps; dev port <code>:5183</code>)</dd>
<dt>Charts</dt><dd>Hand-rolled SVG in <code>components/charts.jsx</code> (LineChart, BarChart, Funnel, Heatmap) &mdash; no charting library</dd>
<dt>API target</dt><dd><code>VITE_ADMIN_API_URL</code> &rarr; <code>AdminWebsiteApi</code> (dev <code>:5336</code>)</dd>
</div>
<p>The dashboard presents platform analytics through a consistent, filter-driven UI. Every page fetches
its metrics from the admin API and renders them with the hand-built SVG charts. A global filter bar
(persisted to <code>localStorage</code>) drives date range, granularity, comparison mode, and segment
filters across every view.</p>

<h2 id="api">Admin API</h2>
<p><code>AdminWebsiteApi</code> shares the same Startup/versioning/Swagger/exception scaffolding as the
public API and the <strong>same shared <code>DataContext</code></strong>, but its services
(<code>Services.AdminCore</code>) are heavy read-only analytics that compute windowed vs prior-period vs
year-over-year comparisons directly against EF Core.</p>
<div class="table-wrap"><table>
<thead><tr><th>Controller</th><th>Route</th><th>Purpose</th></tr></thead>
<tbody>
<tr><td><code>ExecutiveController</code></td><td><code>executive/summary</code></td><td>KPI tiles, growth line, funnel, activity heatmap, revenue trend, needs-attention</td></tr>
<tr><td><code>GrowthController</code></td><td><code>growth/summary</code></td><td>Registrations/activation, cohort retention, by profession/state, campaign conversion</td></tr>
<tr><td><code>LiquidityController</code></td><td><code>liquidity/summary</code></td><td>Marketplace liquidity: application funnel, jobs posted vs filled, supply/demand, time-to-fill</td></tr>
<tr><td><code>LookupController</code></td><td><code>lookup/{{profession|state|candidate-title}}</code></td><td>Filter-bar dropdown data</td></tr>
</tbody></table></div>
<p>All summary endpoints take a validated <code>DashboardFilterModel</code> (date range, granularity,
comparison mode, segment filters) from the query string; <code>DashboardBucketing</code> handles
time-bucketing.</p>

<h2 id="pages">Dashboard pages</h2>
<p>Eleven sidebar tabs: Executive, Growth, Liquidity, Engagement, Employer Activity, Candidate Supply,
Work &amp; Timesheets (GMV), Revenue, Content &amp; Comms, Operational Health, Investor View. Each reads the
global filter, calls its <code>…/summary</code> endpoint, and renders a KPI grid + charts.</p>

<div class="shots">
  <figure><img src="{IMG}/candidate-pricing.png" alt="Candidate pricing"><figcaption>Candidate pricing (product model)</figcaption></figure>
  <figure><img src="{IMG}/employer-pricing.png" alt="Employer pricing"><figcaption>Employer pricing (product model)</figcaption></figure>
</div>
<p class="dgm-cap">Monetization/product context that the analytics dashboards track (from marketing).</p>
""")


# ==========================================================================
OPS = ("ops",
    "Operations",
    "Operations",
    "How to configure and run the platform locally, the key configuration settings, and the external "
    "services the platform depends on.",
    f"""
<h2 id="run">Running locally</h2>
<ul>
<li><strong>Backend:</strong> open <code>locumfy.sln</code> (.NET 10). Run <code>Nullref.Locumfy.WebsiteApi</code>
(dev <code>:5236</code>) and, for dashboards, <code>Nullref.Locumfy.AdminWebsiteApi</code> (dev <code>:5336</code>).
With no connection string configured, the API uses an in-memory database seeded by
<code>DemoDataSeeder</code>, so the apps work out of the box. Swagger UI: <code>/api/swagger</code>.</li>
<li><strong>Website:</strong> <code>npm install &amp;&amp; npm run dev</code> in <code>Nullref.Locumfy.Website</code>
(Vite). Point <code>VITE_API_URL</code> at the API if not on the default port.</li>
<li><strong>Admin site:</strong> same, in <code>Nullref.Locumfy.Adminsite</code> (dev <code>:5183</code>);
defaults to mock data (<code>VITE_ADMIN_DATA_MODE=real</code> to go live).</li>
<li><strong>Mobile:</strong> <code>flutter pub get</code> then run in <code>Nullref.Locumfy.Mobile</code>.
Android emulator reaches the API at <code>10.0.2.2:5236</code>.</li>
</ul>

<h2 id="config">Configuration</h2>
<div class="table-wrap"><table>
<thead><tr><th>Setting</th><th>Where</th><th>Effect</th></tr></thead>
<tbody>
<tr><td><code>ConnectionStrings:Default</code></td><td>API appsettings</td><td>DB connection; empty &rarr; in-memory + demo seed</td></tr>
<tr><td><code>DemoData:Seed</code></td><td>API appsettings</td><td>Seed demo data (default true)</td></tr>
<tr><td><code>AiGeneration</code> (cloud / local LLM)</td><td>API appsettings</td><td>LLM provider, base URL, model, API key</td></tr>
<tr><td>JWT issuer/audience/secret/expiry</td><td>API appsettings</td><td><code>TokenService</code> configuration</td></tr>
<tr><td><code>VITE_API_URL</code> / <code>VITE_ADMIN_API_URL</code> / <code>VITE_ADMIN_DATA_MODE</code></td><td>Frontend env</td><td>API targets &amp; admin data mode</td></tr>
</tbody></table></div>

<h2 id="external">External dependencies</h2>
<p>Operational surfaces to monitor and configure: <strong>AWS</strong> S3 (KMS-encrypted document store),
SQS; <strong>LLM</strong> a configurable cloud model or a self-hosted open-source model (Ollama); an <strong>OCR web service</strong> for
image-only PDFs; and <strong>NPI registry / geolocation</strong> lookups (via the shared
<code>Nullref.Geolocation</code> client) used in candidate onboarding.</p>
""")


PART2_PAGES = [SERVICES, WORKFLOWS, AI, WEB, MOBILE, ADMIN, OPS]

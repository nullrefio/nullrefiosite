# -*- coding: utf-8 -*-
"""Page bodies: Overview, Architecture, Data Layer, REST API."""
from _diagrams import DIAGRAMS


def dia(key, cap):
    return f'<div class="diagram">{DIAGRAMS[key]()}</div>\n<p class="dgm-cap">{cap}</p>'


# ==========================================================================
INDEX = ("index",
    "Locumfy Platform Overview",
    "Overview",
    "A professional network and staffing marketplace for medical providers — a "
    "&ldquo;LinkedIn for healthcare&rdquo; that turns hundreds of thousands of existing resumes into an "
    "engagement, job-search, and credentialing platform.",
    f"""
<!-- MAINTAINER: This is the landing page. Keep the vision paragraph and the tech-stack
     table in sync with reality as the platform evolves. The card grid links to every
     top-level section; add a card here when you add a section. -->

<h2 id="what">What Locumfy is</h2>
<p>Locumfy is a web site and companion mobile application that acts as a professional network and
work marketplace for medical professionals &mdash; nurses, therapists, physicians, advanced
practitioners, pharmacists, and related specialties. It takes the large resume corpus already held
across the Jackson family of staffing companies and uses advanced resume parsing to build a
composite, aggregated profile platform that drives engagement, loyalty, and brand recognition.</p>

<p>The existing Jackson brands are segmented by profession (nurses, therapists, physicians, and so
on). Locumfy <strong>does not replace</strong> that strategy &mdash; it augments it, adding a unified
surface for job search, professional connections, messaging, timesheets, billing, and other ancillary
functionality. The same resume-parsing technology also enables a standardized &ldquo;Jackson format&rdquo;
resume with the ability to <strong>auto-anonymize</strong> resumes for third-party submission to
hospitals and facilities &mdash; removing the manual, inconsistent reformatting recruiters do today.</p>

<div class="callout note"><span class="h">Audience</span>
This documentation is written for the software developers and architects building and extending the
platform. It describes the layers, applications, domain workflows, and the AI/resume subsystem, and
flags known technical debt so you can plan around it.</div>

<h2 id="context">System context</h2>
{dia("system_context",
     "How the three client apps, two REST APIs, shared service/data layers, and external services fit together.")}

<h2 id="map">Documentation map</h2>
<div class="card-grid">
  <a class="card" href="architecture.html"><div class="ic">&#127959;&#65039;</div><h4>System Architecture</h4><p>The layered model, the 20-project solution, and the dependency graph.</p></a>
  <a class="card" href="data-layer.html"><div class="ic">&#128451;&#65039;</div><h4>Data Layer</h4><p>EF Core code-first model, ~120 entities, conventions, and core domains.</p></a>
  <a class="card" href="rest-api.html"><div class="ic">&#128225;</div><h4>REST API</h4><p>The single versioned API, JWT auth, conventions, and the endpoint inventory.</p></a>
  <a class="card" href="service-layer.html"><div class="ic">&#9881;&#65039;</div><h4>Service Layer</h4><p>Feature-sliced services, validation engine, resolvers, and DI.</p></a>
  <a class="card" href="domain-workflows.html"><div class="ic">&#128260;</div><h4>Domain Workflows</h4><p>Job-application state machine, timesheet lifecycle, and resume flows.</p></a>
  <a class="card" href="ai-resume.html"><div class="ic">&#129302;</div><h4>AI &amp; Resume Engine</h4><p>Parsing, structuring, standardized/anonymized resumes, and LLM features.</p></a>
  <a class="card" href="web-frontend.html"><div class="ic">&#128421;&#65039;</div><h4>Web Frontend</h4><p>The React + Vite candidate/employer SPA.</p></a>
  <a class="card" href="mobile-app.html"><div class="ic">&#128241;</div><h4>Mobile App</h4><p>The Flutter/Dart companion app.</p></a>
  <a class="card" href="admin-analytics.html"><div class="ic">&#128202;</div><h4>Admin &amp; Analytics</h4><p>The internal metrics dashboard and its API.</p></a>
  <a class="card" href="operations-security.html"><div class="ic">&#9881;&#65039;</div><h4>Operations</h4><p>Configuration, running the platform locally, and external dependencies.</p></a>
</div>

<h2 id="stack">Technology at a glance</h2>
<div class="table-wrap"><table>
<thead><tr><th>Concern</th><th>Choice</th></tr></thead>
<tbody>
<tr><td>Backend runtime</td><td><strong>.NET 10</strong> (<code>net10.0</code>), ASP.NET Core</td></tr>
<tr><td>API style</td><td>RESTful, URL-path versioned (<code>/api/v1/</code>), OpenAPI/Swagger</td></tr>
<tr><td>Auth</td><td>Self-issued JWT (no third-party IdP); roles <code>candidate</code> / <code>facility</code></td></tr>
<tr><td>Persistence</td><td>Entity Framework Core 10, code-first (relational database)</td></tr>
<tr><td>Web frontend</td><td>React 18 + Vite 5 + react-router 6 (no TypeScript)</td></tr>
<tr><td>Mobile</td><td>Flutter + Dart 3.11</td></tr>
<tr><td>Admin site</td><td>React 18 + Vite 5 (mock-or-live data modes)</td></tr>
<tr><td>AI / LLM</td><td>Configurable cloud LLM or local open-source model (Ollama); prompt-built from candidate data</td></tr>
<tr><td>Resume parsing</td><td>Custom engine + UglyToad.PdfPig, DocumentConversion, Sovren SRP (backstop)</td></tr>
<tr><td>Document/PDF generation</td><td>PuppeteerSharp (HTML&rarr;PDF), PdfSharp</td></tr>
<tr><td>Cloud storage</td><td>AWS S3 (KMS-encrypted document storage), SQS</td></tr>
<tr><td>Logging</td><td>Serilog</td></tr>
</tbody></table></div>

<div class="callout tip"><span class="h">Web &amp; mobile mirror each other</span>
The website and mobile app intentionally offer the same feature set against the same REST contract.
When you change a feature that spans both, update them in parallel.</div>
""")


# ==========================================================================
ARCHITECTURE = ("architecture",
    "System Architecture",
    "Architecture",
    "Locumfy is a layered, feature-sliced .NET solution of ~20 projects, fronted by three "
    "independent client apps and two REST APIs, all sharing one Entity Framework Core data model.",
    f"""
<h2 id="layers">Layered model</h2>
<p>The platform follows a conventional layered architecture. Presentation clients talk only to the
REST APIs; the APIs are thin and delegate to a feature-sliced service layer; the service layer is the
only thing that touches the Entity Framework Core data layer. A set of cross-cutting libraries
(validation, AWS, shared framework packages) is available to every layer.</p>
{dia("layers", "The five architectural layers and the cross-cutting libraries that support them.")}

<h2 id="solution">The solution</h2>
<p>Everything lives in one Visual Studio solution rooted at <code>C:\\code\\locumfy\\src</code>
(<code>locumfy.sln</code>). The backend projects target <strong>.NET 10</strong> and use central NuGet
version management via <code>Directory.Packages.props</code>. Internal shared libraries
(<code>Nullref.Common.*</code>, <code>Nullref.EFCore.Extensions</code>,
<code>Nullref.Geolocation.*</code>) are consumed as compiled packages from a private feed
(<code>nuget.config</code>) &mdash; they are <em>not</em> in this source tree.</p>

<div class="table-wrap"><table>
<thead><tr><th>Project</th><th>Layer</th><th>Purpose</th></tr></thead>
<tbody>
<tr><td><code>Nullref.Locumfy.Website</code></td><td>Presentation</td><td>React SPA for candidates &amp; employers</td></tr>
<tr><td><code>Nullref.Locumfy.Mobile</code></td><td>Presentation</td><td>Flutter companion app</td></tr>
<tr><td><code>Nullref.Locumfy.Adminsite</code></td><td>Presentation</td><td>React internal analytics dashboard</td></tr>
<tr><td><code>Nullref.Locumfy.WebsiteApi</code></td><td>API</td><td>Public REST API (mobile + website)</td></tr>
<tr><td><code>Nullref.Locumfy.AdminWebsiteApi</code></td><td>API</td><td>Admin dashboard REST API</td></tr>
<tr><td><code>...DataProvider.Services.Core</code></td><td>Service</td><td>Feature-sliced services for the public API</td></tr>
<tr><td><code>...DataProvider.Services.AdminCore</code></td><td>Service</td><td>Analytics/KPI services for the admin API</td></tr>
<tr><td><code>...DataProvider.Services.ResumeBuilder</code></td><td>Service</td><td>Standardized/anonymized resume generation</td></tr>
<tr><td><code>...DataProvider.DataStorage</code></td><td>Data</td><td>EF Core entities + <code>DataContext</code></td></tr>
<tr><td><code>...DataProvider.DataStorage.Migrations</code></td><td>Data</td><td>EF Core migrations project</td></tr>
<tr><td><code>Nullref.Locumfy.Parsing</code></td><td>Subsystem</td><td>Resume text extraction &amp; parsing engine</td></tr>
<tr><td><code>Nullref.Locumfy.Parsing.PdfUtils</code></td><td>Subsystem</td><td>PdfPig-based PDF text extraction</td></tr>
<tr><td><code>Nullref.Locumfy.ResumeParser</code></td><td>Subsystem</td><td>Parsed resume &rarr; persisted candidate data</td></tr>
<tr><td><code>Nullref.Locumfy.AiData</code></td><td>Subsystem</td><td>LLM prompt construction from candidate data</td></tr>
<tr><td><code>Nullref.Locumfy.ResumeExportTraining</code></td><td>Tooling</td><td>Console exporter of ML training pairs</td></tr>
<tr><td><code>Nullref.Locumfy.Infrastructure</code></td><td>Cross-cutting</td><td>Validation engine, extensions, attributes</td></tr>
<tr><td><code>Nullref.Locumfy.AwsCore</code></td><td>Cross-cutting</td><td>AWS S3/KMS/SQS integration</td></tr>
<tr><td colspan="3"><em>Plus test harnesses:</em> <code>...Services.Core.Tests</code>, <code>...WebsiteApi.Tests</code>,
<code>...DataStorage.TestHarness</code>, <code>...TestHarness</code>.</td></tr>
</tbody></table></div>

<h2 id="deps">Project dependency graph</h2>
{dia("dependency_graph",
     "ProjectReferences between the backend assemblies. The public API funnels through Services.Core; everything ultimately depends on DataStorage.")}

<div class="callout note"><span class="h">Composition detail</span>
<code>WebsiteApi.csproj</code> declares a ProjectReference only to <code>Services.Core</code> (plus the
shared Swagger package). <code>AwsCore</code> is pulled in at startup by assembly scanning
(<code>Startup</code> calls <code>.Include&lt;AwsServiceInstaller&gt;()</code>) rather than a hard
reference &mdash; keep that in mind when tracing dependencies.</div>

<h2 id="request">Request flow</h2>
<p>A typical authenticated request travels: <strong>client</strong> &rarr; <code>Bearer</code> JWT on an
<code>/api/v1/&hellip;</code> route &rarr; <strong>controller</strong> (thin; validates attributes, reads
<code>CurrentUserId</code>/<code>CurrentRole</code>) &rarr; <strong>feature service</strong> (business
logic, model validation, entity&rarr;UI-model mapping) &rarr; <strong>DataContext</strong> (EF Core) &rarr;
database. Errors are thrown as typed exceptions and mapped to HTTP status codes by a global middleware
(see <a href="rest-api.html#errors">REST API &rsaquo; Error handling</a>).</p>

<h2 id="crosscutting">Cross-cutting libraries</h2>
<div class="kv">
<dt>Infrastructure</dt><dd>The validation engine (<code>ValidatableObjectExtensions.Validate&lt;T&gt;()</code>), common extensions (hashing, formatting), HTML sanitization, and custom attributes. No project references &mdash; depends only on the ASP.NET Core framework reference and shared packages.</dd>
<dt>AwsCore</dt><dd><code>DocumentS3Service</code> (tenant-scoped, KMS-encrypted S3 document store) and <code>AwsServiceInstaller</code> which registers <code>IAmazonS3</code>/<code>IAmazonSQS</code>. Uploaded candidate/company documents are stored in AWS S3.</dd>
<dt>Nullref.Common.*</dt><dd>Private shared packages: <code>ModelBases</code> (<code>IModel</code>, validation bases, <code>IUserContextService</code>, exception types), <code>DependencyInjection</code> (<code>[ScopedLifetime]</code>, Scrutor-based installers), <code>Caching</code>, <code>Logging</code>, <code>Serialization</code>, <code>SwaggerConfiguration</code>.</dd>
<dt>Nullref.EFCore.Extensions</dt><dd>The <code>ContextBase</code> that <code>DataContext</code> derives from, plus attributes like <code>[MaxLengthUnbounded]</code> and <code>[ModelIgnore]</code>.</dd>
</div>

<div class="callout note"><span class="h">Database provider</span>
The data layer is EF Core code-first against a relational database. In development, when no connection
string is configured, the API uses an in-memory provider seeded with demo data so the apps run out of
the box.</div>
""")


# ==========================================================================
DATA = ("data",
    "Data Layer",
    "Data Layer",
    "Entity Framework Core 10, code-first. Roughly 120 entities model candidates and their rich "
    "profiles, employers and jobs, the application/timesheet workflow, messaging, networking, and a "
    "large amount of operational and lookup data.",
    f"""
<div class="toc"><strong>On this page</strong>
<ul>
<li><a href="#context">DataContext &amp; conventions</a></li>
<li><a href="#domains">Core data domains</a></li>
<li><a href="#entity">Entity conventions</a></li>
<li><a href="#enums">Domain enums</a></li>
<li><a href="#migrations">Migrations</a></li>
</ul></div>

<h2 id="context">DataContext &amp; conventions</h2>
<p>The single <code>DataContext</code> (project <code>Nullref.Locumfy.DataProvider.DataStorage</code>)
derives from <code>Nullref.EFCore.Extensions.ContextBase</code>. Notable choices:</p>
<ul>
<li><strong>Lazy loading is disabled everywhere</strong> &mdash; <code>ChangeTracker.LazyLoadingEnabled = false</code>
and <code>UseLazyLoadingProxies(false)</code>. Load related data explicitly with <code>Include</code>/projections.</li>
<li>Each entity is exposed as a <strong>singular</strong>, <code>protected set</code> <code>DbSet&lt;T&gt;</code>
(e.g. <code>public DbSet&lt;Candidate&gt; Candidate</code>, not <code>Candidates</code>).</li>
<li>Model configuration is discovered by assembly scan:
<code>modelBuilder.ApplyConfigurationsFromAssembly(&hellip;)</code> &mdash; there are no manual
<code>HasOne</code>/<code>HasMany</code> calls in the context itself.</li>
</ul>
<pre><code><span class="tok-k">public class</span> <span class="tok-t">DataContext</span> : Nullref.EFCore.Extensions.ContextBase
{{
    <span class="tok-k">public</span> DbSet&lt;<span class="tok-t">Candidate</span>&gt; Candidate {{ <span class="tok-k">get</span>; <span class="tok-k">protected set</span>; }}
    <span class="tok-k">public</span> DbSet&lt;<span class="tok-t">Job</span>&gt; Job {{ <span class="tok-k">get</span>; <span class="tok-k">protected set</span>; }}
    <span class="tok-c">// ~120 DbSets total …</span>
}}</code></pre>

<h2 id="domains">Core data domains</h2>
<p>Although the model is broad, it clusters into a handful of domains. The <code>Candidate</code> entity
is the center of gravity: it implements <code>IUserAccount</code> and owns ~18 satellite tables that
together form the rich professional profile.</p>
{dia("data_domains",
     "Entity clusters. Candidate is the profile hub; Company→Employer→Job→JobApplication→Timesheet is the marketplace spine; messaging, feed, network, and documents provide engagement.")}

<div class="table-wrap"><table>
<thead><tr><th>Domain</th><th>Representative entities</th></tr></thead>
<tbody>
<tr><td>Candidate profile</td><td><code>Candidate</code>, <code>CandidateEmployment</code>, <code>CandidateEducation</code>, <code>CandidateCertification(Adv)</code>, <code>CandidateStateLicense</code>, <code>CandidateSkill</code>, <code>CandidateLanguage</code>, <code>CandidateAward</code>, <code>CandidateResearch</code>, <code>CandidatePublication</code>, <code>CandidatePresentation</code>, <code>CandidateReference</code>, <code>CandidateResidency</code>, <code>CandidateInternship</code>, <code>CandidateMembership</code>, <code>CandidateVolunteer</code>, <code>CandidateSpecialty</code>, <code>CandidateStateGeoPref</code></td></tr>
<tr><td>Employer &amp; marketplace</td><td><code>Company</code>, <code>Employer</code>, <code>Job</code>, <code>JobApplication</code>, <code>JobApplicationTerm</code>, <code>Timesheet</code>, <code>TimesheetNote</code>, <code>Rating</code>/<code>JobUserRating</code></td></tr>
<tr><td>Networking &amp; engagement</td><td><code>CandidateNetwork</code>, <code>CandidateNetworkRequest</code>, <code>CandidateNetworkSuggestion</code>, <code>MemberPost</code>, <code>CompanyFeed</code>, <code>MessageThread</code>, <code>Message</code>, <code>News</code>, <code>Article</code></td></tr>
<tr><td>Documents &amp; resume</td><td><code>Document</code>, <code>CompanyDocument</code>, <code>DocumentType</code>, <code>ResumeCreate</code>, <code>ResumeNakedCache</code>, <code>CandidateAiVerification</code>, <code>CandidateSearchData</code></td></tr>
<tr><td>Commerce</td><td><code>Product</code>, <code>ProductGroup</code>, <code>OrderBundle</code>, <code>Transaction</code>, <code>TransactionDetail</code>, <code>Insurance</code></td></tr>
<tr><td>Lookup / reference</td><td><code>Profession</code>, <code>Specialty</code>, <code>SpecialtyAlias</code>, <code>State</code>, <code>Gender</code>, <code>Language</code>, <code>CandidateTitleType</code>, <code>NpiData</code></td></tr>
<tr><td>Ops / security / audit</td><td><code>UserAccount</code>, <code>Administrator</code>, <code>ApiToken</code>, <code>SessionTracking</code>, <code>UserActivityLog</code>, <code>ErrorLog</code>, <code>EmailLog</code>, <code>SmsLog</code>, <code>PageLog</code>, <code>BlockedIpAddress</code>, <code>IpLookup</code></td></tr>
</tbody></table></div>

<h2 id="entity">Entity conventions</h2>
<p>These conventions are enforced by project rules; follow them when adding entities.</p>
<div class="kv">
<dt>Base classes</dt><dd>Inherit an audit base: <code>AuditableEntityBase2</code> (Created + Modified), <code>AuditableCreatedModifiedEntityBase</code>, or <code>AuditableModifiedEntityBase</code>. All implement <code>IEntity</code>; account entities also implement <code>IUserAccount</code>.</dd>
<dt>Primary keys</dt><dd><code>[Key, DatabaseGenerated(DatabaseGeneratedOption.Identity)]</code> with an <code>internal set</code>. Named <code>{{Entity}}Id</code>, or <code>RowId</code> for junction/lookup rows.</dd>
<dt>Required scalars</dt><dd>Every non-nullable value-type property is marked <code>[Required]</code>. Nullable scalars are not.</dd>
<dt>Strings</dt><dd>Every string has <code>[MaxLength(n)]</code> or <code>[MaxLengthUnbounded]</code>. Entities with many strings centralize limits in an inner <code>readonly struct MaxLengthValues</code>.</dd>
<dt>Enums</dt><dd>Stored as <code>int</code>; a <code>[NotMapped]</code> converter property gives typed access (e.g. <code>JobCompletedTypeValue</code>).</dd>
<dt>Navigations</dt><dd>Collection navigations are initialized <code>= []</code> and named with a <code>List</code> suffix (<code>JobApplicationList</code>). Configured in the companion <code>Configuration/</code> class with an explicit <code>OnDelete</code>.</dd>
<dt>Owned JSON</dt><dd>Complex nested objects are serialized to a single column via <code>builder.OwnsOne(&hellip;).ToJson()</code> (e.g. <code>Timesheet.ConfigXml</code>).</dd>
</div>

<div class="callout tip"><span class="h">Configuration pattern</span>
One <code>IEntityTypeConfiguration&lt;T&gt;</code> per entity in <code>Configuration/</code>. Relationships,
delete behavior, and owned-type mapping live there &mdash; never inline in the entity or the context.
Most relationships use <code>DeleteBehavior.Restrict</code>; optional FKs use <code>SetNull</code>.</div>

<h2 id="enums">Domain enums (<code>Types.cs</code>)</h2>
<p>Enums use a <code>Constants</code> suffix, explicit integer values, and <code>[Display(Name=…)]</code>.
The most important ones:</p>
<div class="table-wrap"><table>
<thead><tr><th>Enum</th><th>Values</th><th>Used by</th></tr></thead>
<tbody>
<tr><td><code>ProfessionConstants</code></td><td>Physician (1), Therapy (2), Nursing (3), Counseling &amp; Social Services (5), Advanced Practitioner (6), Pharmacy (7)</td><td>Candidate segmentation, specialties</td></tr>
<tr><td><code>CandidateTitleTypeConstants</code></td><td>MD, DO, PA, NP, CRNA, RN, LVN/LPN, DDS, DMD, DPM, Pharmacist, PSY.D, Ph.D, CNM, CNA, Technologist, Social Worker/Counselor, Executive, &hellip;</td><td>Candidate title</td></tr>
<tr><td><code>JobCompletedTypeConstants</code></td><td>None (1), Provider_Accepted (2), Provider_Rejected (3), Facility_Accepted (4), FacilityRejected (5), Complete (6)</td><td>Job-application state machine</td></tr>
<tr><td><code>DocumentTypeConstants</code></td><td>References, State licenses, DL/Passport, W9, Photo, CV, DEA, State Controlled Substance, BLS, ACLS, ATLS, PALS, MMR, TB, Drug screen, Misc, Internal</td><td>Uploaded credential documents</td></tr>
<tr><td><code>ResumeSearchLogActionTypeConstants</code></td><td>Add/Delete/Change Note, Forward Info, Contact Candidate, Change Status, View Candidate, Download Resume, Save/Unsave Candidate</td><td>Recruiter activity logging</td></tr>
</tbody></table></div>
<p>Timesheet states are seeded rows / constants rather than a <code>Types.cs</code> enum:
<code>Open=1, ProviderApproved=2, ClientApproved=3, Rejected=4, Paid=5</code>.</p>

<h2 id="migrations">Migrations</h2>
<p>Migrations are code-first and live in the separate
<code>Nullref.Locumfy.DataProvider.DataStorage.Migrations</code> project. In development, when no
connection string is configured the API uses an EF Core <em>in-memory</em> database seeded by
<code>DemoDataSeeder</code>, so the apps run with realistic demo data out of the box.</p>

<div class="callout todo"><span class="h">Maintainer note</span>
This page lists <em>representative</em> entities, not all ~120. When you add a new domain area, add a
row to the &ldquo;Core data domains&rdquo; table and, if it introduces a new cluster, extend the
<code>data_domains</code> diagram in <code>_diagrams.py</code>. Consider auto-generating a full entity
index from the <code>Entity/</code> folder if the model keeps growing.</div>
""")


# ==========================================================================
API = ("api",
    "REST API",
    "REST API",
    "A single ASP.NET Core API (Nullref.Locumfy.WebsiteApi) serves both the website and the mobile "
    "app. Convention-driven controllers, self-issued JWT auth, and a global exception-to-HTTP mapping "
    "keep the surface consistent.",
    f"""
<div class="toc"><strong>On this page</strong>
<ul>
<li><a href="#conventions">Controller conventions</a></li>
<li><a href="#auth">Authentication &amp; roles</a></li>
<li><a href="#errors">Error handling</a></li>
<li><a href="#endpoints">Endpoint inventory</a></li>
<li><a href="#swagger">Swagger / OpenAPI</a></li>
</ul></div>

<p>Base path <code>api/v1/</code>. Versioning is by URL path (<code>[ApiVersion("1")]</code>). JSON in and
out, camelCase, with NodaTime types serialized via <code>MicroElements.Swashbuckle.NodaTime</code>.</p>

<h2 id="conventions">Controller conventions</h2>
<p>All controllers derive from <code>ApiControllerBase</code>, which supplies
<code>CurrentUserId</code>, <code>CurrentEmail</code>, and <code>CurrentRole</code> from the validated
token. Routes are built from a <code>ControllerMainPath</code> const and sub-path consts, with
<code>nameof()</code> used for route variables.</p>
<pre><code><span class="tok-n">[SwaggerOperation(Summary = <span class="tok-s">"Creates a new candidate account."</span>)]</span>
<span class="tok-n">[HttpPost]</span> <span class="tok-n">[AllowAnonymous]</span>
<span class="tok-k">public async</span> Task&lt;ActionResult&lt;<span class="tok-t">LoginReturnModel</span>&gt;&gt; CreateAccount(
    <span class="tok-n">[Required, FromBody]</span> <span class="tok-t">CandidateCreateModel</span> model)
    =&gt; Ok(<span class="tok-k">await</span> _candidateService.CreateAccount(model));</code></pre>
<p>Two rules matter most for correctness:</p>
<ul>
<li><strong>Every parameter</strong> carries <code>[Required]</code> <em>and</em> a binding source
(<code>[FromBody]</code>/<code>[FromRoute]</code>/<code>[FromQuery]</code>/<code>[FromForm]</code>).</li>
<li><strong>The method-name prefix drives the HTTP status code</strong>, enforced by the
<code>DefaultApiResponses</code> API conventions. Never name an action outside the scheme.</li>
</ul>
<div class="table-wrap"><table>
<thead><tr><th>Prefix</th><th>Success code</th><th>Prefix</th><th>Success code</th></tr></thead>
<tbody>
<tr><td><code>Get*</code></td><td>200 OK</td><td><code>Update*</code></td><td>200 OK</td></tr>
<tr><td><code>GetNoReturn*</code></td><td>204</td><td><code>UpdateNoReturn*</code></td><td>204</td></tr>
<tr><td><code>GetFile*</code></td><td>200 (file)</td><td><code>Delete*</code></td><td>204</td></tr>
<tr><td><code>Create*</code></td><td>201 Created</td><td><code>Upload*</code></td><td>200</td></tr>
<tr><td><code>CreateNoReturn*</code></td><td>204</td><td><code>Execute*</code></td><td>200</td></tr>
<tr><td><code>Queue*</code> / <code>*Accepted</code></td><td>202 Accepted</td><td colspan="2"><em>No <code>Async</code> suffix on method names, ever.</em></td></tr>
</tbody></table></div>

<h2 id="auth">Authentication &amp; roles</h2>
<div class="kv">
<dt>Scheme</dt><dd>Self-generated JWT bearer (HMAC-SHA256). No Google/Facebook/third-party IdP.</dd>
<dt>Roles</dt><dd><code>TokenService.RoleCandidate</code> (<code>candidate</code>) and <code>TokenService.RoleFacility</code> (<code>facility</code>).</dd>
<dt>Obtaining a token</dt><dd><code>POST /api/v1/login</code> returns a <code>LoginReturnModel</code>. There is no silent refresh; the client explicitly calls <code>POST /api/v1/login/renew</code>.</dd>
<dt>Per-request check</dt><dd><code>JwtBearerEvents.OnTokenValidated</code> verifies the user exists and pushes <code>UserId</code> into the scoped <code>IUserContextService</code>.</dd>
<dt>Guarding actions</dt><dd><code>[AllowAnonymous]</code>, <code>[Authorize]</code>, or <code>[Authorize(Roles = TokenService.RoleCandidate|RoleFacility)]</code>.</dd>
</div>

<h2 id="errors">Error handling</h2>
<p>Services throw typed exceptions; <code>ExceptionHandlerMiddleware</code> maps them to HTTP responses,
so controllers don&rsquo;t add <code>[ProducesResponseType]</code> for the standard error codes.</p>
<div class="table-wrap"><table>
<thead><tr><th>Exception</th><th>HTTP</th><th>Exception</th><th>HTTP</th></tr></thead>
<tbody>
<tr><td><code>EntityNotFoundException</code></td><td>404</td><td><code>UnauthorizedException</code></td><td>401</td></tr>
<tr><td><code>EntityInUseException</code></td><td>409</td><td><code>ForbiddenException</code></td><td>403</td></tr>
<tr><td><code>RequestValidationException</code></td><td>422</td><td><code>BadRequestException</code></td><td>400</td></tr>
</tbody></table></div>
<p>422 responses carry an <code>UnprocessableEntityResponseModel</code> with per-field validation
errors produced by the <a href="service-layer.html#validation">validation engine</a>.</p>

<h2 id="endpoints">Endpoint inventory</h2>
<p>Role column: <span class="pill role">C</span> candidate, <span class="pill role">F</span> facility,
<span class="pill gray">Anon</span> anonymous, <span class="pill">Auth</span> any authenticated user.
Routes below omit the <code>api/v1/</code> prefix.</p>

<h3 id="ep-auth">Login &amp; lookup (anonymous)</h3>
<div class="table-wrap"><table>
<thead><tr><th>Method</th><th>Route</th><th>Role</th><th>Purpose</th></tr></thead>
<tbody>
<tr><td><span class="verb post">POST</span></td><td><code>login</code></td><td><span class="pill gray">Anon</span></td><td>Authenticate candidate or facility &rarr; JWT</td></tr>
<tr><td><span class="verb post">POST</span></td><td><code>login/renew</code></td><td><span class="pill">Auth</span></td><td>Re-issue a fresh JWT for the current user</td></tr>
<tr><td><span class="verb get">GET</span></td><td><code>data/specialty</code> · <code>data/state</code> · <code>data/candidate-title</code> · <code>data/document-type</code> · <code>data/product-group</code></td><td><span class="pill gray">Anon</span></td><td>Lookup/reference data for forms &amp; pricing</td></tr>
<tr><td><span class="verb get">GET</span></td><td><code>data/coi</code></td><td><span class="pill gray">Anon</span></td><td>Download Certificate of Insurance PDF</td></tr>
<tr><td><span class="verb get">GET</span></td><td><code>news</code></td><td><span class="pill gray">Anon</span></td><td>Latest platform news</td></tr>
<tr><td><span class="verb get">GET</span></td><td><code>candidate-profile/{{candidateId}}</code></td><td><span class="pill role">C</span><span class="pill role">F</span></td><td>Public candidate profile (private fields excluded)</td></tr>
</tbody></table></div>

<h3 id="ep-candidate">Candidate API (<code>candidate/*</code>, role candidate)</h3>
<div class="table-wrap"><table>
<thead><tr><th>Area</th><th>Representative endpoints</th></tr></thead>
<tbody>
<tr><td>Account</td><td><code>POST candidate</code>, <code>POST candidate/create-account</code>, <code>POST candidate/create-account-npi</code>, <code>GET/PUT candidate/me</code>, <code>GET candidate/profile</code>, <code>GET candidate/npi</code>, <code>POST candidate/ai-summary</code></td></tr>
<tr><td>Jobs</td><td><code>GET candidate/job-search</code>, <code>GET candidate/job-saved</code>, <code>GET candidate/job-applied</code>, <code>POST candidate/job/{{jobId}}/save</code> · <code>/unsave</code> · <code>/apply</code></td></tr>
<tr><td>Applications</td><td><code>POST candidate/application/{{id}}/accept</code> · <code>/reject</code></td></tr>
<tr><td>Network</td><td><code>GET candidate/network</code> · <code>network-request</code> · <code>network-suggestion</code>; <code>POST …/{{id}}/connect</code> · <code>/accept</code> · <code>/dismiss</code></td></tr>
<tr><td>Feed</td><td><code>GET/POST candidate/feed</code>, <code>POST candidate/feed/{{postId}}/like</code></td></tr>
<tr><td>Messaging</td><td><code>GET candidate/message</code>, <code>GET candidate/message-thread/{{threadId}}</code>, <code>POST candidate/message</code>, read-receipts</td></tr>
<tr><td>Timesheets</td><td><code>GET/POST candidate/timesheet</code>, <code>PUT …/{{id}}</code>, <code>POST …/{{id}}/submit</code>, notes CRUD, <code>GET …/{{id}}/html</code> · <code>/pdf</code></td></tr>
<tr><td>Documents</td><td><code>GET candidate/document</code>, <code>…/{{id}}/download</code>, <code>POST …/upload</code>, <code>POST …/resume-upload</code> (parses &amp; auto-fills profile), <code>DELETE …/{{id}}</code>, <code>POST candidate/w9</code></td></tr>
<tr><td>Profile sub-resources</td><td>Full CRUD (<code>GET/{{id}}</code>, <code>POST</code>, <code>PUT/{{id}}</code>, <code>DELETE/{{id}}</code>) for <code>employment</code>, <code>education</code>, <code>certification</code>, <code>award</code>, <code>internship</code>, <code>skill</code>, <code>volunteer</code>, <code>state-license</code>, <code>research</code>, <code>residency</code>, <code>reference</code>, <code>presentation</code>, <code>publication</code>, <code>membership</code>, <code>language</code>, <code>specialty</code>, plus <code>state-geo-pref</code></td></tr>
<tr><td>Exports</td><td><code>GET candidate/agreement-download</code>, <code>GET candidate/profile-html</code> · <code>profile-pdf</code></td></tr>
</tbody></table></div>

<h3 id="ep-employer">Employer API (<code>employer/*</code>, role facility)</h3>
<div class="table-wrap"><table>
<thead><tr><th>Area</th><th>Representative endpoints</th></tr></thead>
<tbody>
<tr><td>Account</td><td><code>POST employer</code>, <code>GET/PUT employer/me</code></td></tr>
<tr><td>Jobs</td><td><code>GET employer/job</code>, <code>POST employer/job</code>, <code>PUT employer/job/{{jobId}}</code>, <code>DELETE employer/job/{{jobId}}</code></td></tr>
<tr><td>Applications</td><td><code>GET employer/application</code>, <code>GET employer/application/job/{{jobId}}</code>, <code>POST …/{{id}}/accept</code> · <code>/reject</code> · <code>/complete</code></td></tr>
<tr><td>Candidates</td><td><code>GET employer/candidate</code> (search), <code>GET employer/candidate/{{id}}</code>, <code>…/npi</code>, <code>…/ai-summary</code>, <code>…/ai-comments</code>, <code>…/resume</code> (standardized PDF)</td></tr>
<tr><td>Network</td><td><code>GET employer/network-connection</code> · <code>network-suggestion</code>, <code>POST employer/network-invite/{{candidateId}}</code></td></tr>
<tr><td>Messaging / Feed</td><td>thread list &amp; send (mirrors candidate); <code>GET/POST employer/feed</code>, like</td></tr>
<tr><td>Timesheets</td><td><code>GET employer/timesheet</code>, <code>POST …/{{id}}/approve</code> · <code>/reject</code>, <code>GET …/{{id}}/html</code> · <code>/pdf</code></td></tr>
</tbody></table></div>

<h2 id="swagger">Swagger / OpenAPI</h2>
<p>In Development, Swagger UI is served at <code>/api/swagger</code> and the JSON spec at
<code>/api/swagger/v1/swagger.json</code>. Every action has a <code>[SwaggerOperation(Summary=…)]</code>.
The frontend clients are generated/hand-written against this contract.</p>

<div class="callout todo"><span class="h">Maintainer note</span>
The tables above are curated from the controllers (<code>CandidateController</code> alone is ~46&nbsp;KB).
Rather than hand-maintain a full route list here, prefer the live Swagger JSON as the source of truth
and keep this page at the &ldquo;area &rarr; representative endpoints&rdquo; level of detail. If you want a
complete generated table, wire a small step that reads <code>swagger.json</code> and emits an HTML
fragment.</div>
""")

import Hero from '@/components/Hero';
import Analyzer from '@/components/Analyzer';
import FeatureCard from '@/components/FeatureCard';
import StatsSection from '@/components/StatsSection';
import Footer from '@/components/Footer';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 font-sans selection:bg-blue-200 dark:selection:bg-blue-900">

      {/* Hero Section */}
      <Hero />

      {/* Feature Grid */}
      <section id="features" className="py-20 bg-white dark:bg-gray-900">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-extrabold text-gray-900 dark:text-white sm:text-4xl">
              Comprehensive Protection
            </h2>
            <p className="mt-4 text-xl text-gray-500 dark:text-gray-400">
              Our agent detects diverse cyber threats instantly.
            </p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            <FeatureCard
              title="Phishing Detection"
              description="Identifies deceptive links and social engineering tactics aiming to steal credentials."
              icon="alert"
            />
            <FeatureCard
              title="Malware Scanning"
              description="Detects dangerous file signatures and malicious code delivery attempts."
              icon="shield"
            />
            <FeatureCard
              title="Impersonation"
              description="Spots attempts to mimic trusted entities or authority figures."
              icon="user"
            />
            <FeatureCard
              title="Prompt Injection"
              description="Prevents manipulation of AI behavior through adversarial inputs."
              icon="lock"
            />
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <StatsSection />

      {/* Analyzer Section */}
      <section id="analyzer" className="py-24 bg-gray-50 dark:bg-gray-900">
        <div className="max-w-4xl mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
              Try It Yourself
            </h2>
            <p className="mt-4 text-lg text-gray-600 dark:text-gray-300">
              Analyze any message safely in our sandboxed environment.
            </p>
          </div>
          <Analyzer />
        </div>
      </section>

      {/* How it Works */}
      <section className="py-20 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="lg:text-center">
            <h2 className="text-base text-blue-600 font-semibold tracking-wide uppercase">Under the Hood</h2>
            <p className="mt-2 text-3xl leading-8 font-extrabold tracking-tight text-gray-900 dark:text-white sm:text-4xl">
              Deterministic AI Security
            </p>
            <p className="mt-4 max-w-2xl text-xl text-gray-500 dark:text-gray-400 lg:mx-auto">
              We combine large language models with deterministic policy engines to ensure safety, auditability, and speed.
            </p>
          </div>

          <div className="mt-10">
            <dl className="space-y-10 md:space-y-0 md:grid md:grid-cols-2 md:gap-x-8 md:gap-y-10">
              <div className="relative">
                <dt>
                  <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
                    1
                  </div>
                  <p className="ml-16 text-lg leading-6 font-medium text-gray-900 dark:text-white">Deterministic Preprocessing</p>
                </dt>
                <dd className="mt-2 ml-16 text-base text-gray-500 dark:text-gray-400">
                  Every message is first scanned for known malicious patterns, URLs, and keywords using regex and high-speed rule engines.
                </dd>
              </div>
              <div className="relative">
                <dt>
                  <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
                    2
                  </div>
                  <p className="ml-16 text-lg leading-6 font-medium text-gray-900 dark:text-white">AI Threat Reasoning</p>
                </dt>
                <dd className="mt-2 ml-16 text-base text-gray-500 dark:text-gray-400">
                  Gemini 3 Flash analyzes the semantic intent of the message to catch subtle social engineering and zero-day threats.
                </dd>
              </div>
              <div className="relative">
                <dt>
                  <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
                    3
                  </div>
                  <p className="ml-16 text-lg leading-6 font-medium text-gray-900 dark:text-white">Memory Escalation</p>
                </dt>
                <dd className="mt-2 ml-16 text-base text-gray-500 dark:text-gray-400">
                  Our engine tracks repeat offenders. If a threat persists, penalties automatically escalate from warnings to blocks.
                </dd>
              </div>
              <div className="relative">
                <dt>
                  <div className="absolute flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
                    4
                  </div>
                  <p className="ml-16 text-lg leading-6 font-medium text-gray-900 dark:text-white">Secure Audit Logging</p>
                </dt>
                <dd className="mt-2 ml-16 text-base text-gray-500 dark:text-gray-400">
                  Every decision is cryptographically hashed and logged to an append-only ledger for compliance and post-incident forensics.
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </section>

      {/* Footer */}
      <Footer />
    </main>
  );
}

import Navbar from "@/components/navbar";

export default function Home() {
  return (
    <>
      <Navbar />

      <section class="hero is-link is-fullheight-with-navbar">
        <div class="hero-body">
          <div>
            <p class="title">peFET</p>
            <p class="subtitle">Pre-event fast and easy testing</p>
            <p class="subtitle">peFET allows you to easily send notification emails to participants of your event, and collect FET results from them.</p>
          </div>
        </div>
      </section>
    </>
  );
}

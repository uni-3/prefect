<script>
	import '@evidence-dev/tailwind/fonts.css';
	import '../app.css';
	import { EvidenceDefaultLayout } from '@evidence-dev/core-components';
	export let data;
</script>

<EvidenceDefaultLayout
   data={data}
   logo="/uni-3.jpg"
   githubRepo="https://github.com/uni-3/prefect"
   neverShowQueries=true
 >
	<slot slot="content" />
</EvidenceDefaultLayout>

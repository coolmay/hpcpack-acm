namespace Microsoft.HpcAcm.Frontend
{
    using Microsoft.AspNetCore.Builder;
    using Microsoft.AspNetCore.Hosting;
    using Microsoft.AspNetCore.Mvc;
    using Microsoft.Extensions.Configuration;
    using Microsoft.Extensions.DependencyInjection;
    using Serilog;

    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;
        }

        public ILogger Logger { get; }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
           
            services.AddCors();
            services.AddMvc(x => x.EnableEndpointRouting = false).AddJsonOptions(options => {
                options.JsonSerializerOptions.Converters.Add(new System.Text.Json.Serialization.JsonStringEnumConverter());
                options.JsonSerializerOptions.IgnoreNullValues = true;
            });
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IHostingEnvironment env)
        {
            app.UseDefaultFiles();
            app.UseStaticFiles();

            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            app.UseCors(builder =>
                builder.AllowAnyOrigin()
                  .AllowAnyMethod()
                  .AllowAnyHeader()
                  .AllowCredentials()
                  .WithExposedHeaders("Location")
            );

            app.UseMiddleware<ExceptionHandlingMiddleware>();
        }
    }
}

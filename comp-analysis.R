library(dplyr)
library(httr)
library(jsonlite)
library(magrittr)

resp <- GET("https://www.levels.fyi/js/salaryData.json")
cat("Response code: ", resp$status_code, "\n")

if (resp$status_code != 200)
  stop("Failed to fetch data!")

json <- rawToChar(resp$content)
salaries_df <- jsonlite::fromJSON(json) %>%
  filter(
    grepl(", Canada$", location, ignore.case = TRUE),
    title == "Software Engineer",
    as.numeric(yearsofexperience) >= 7,
    as.numeric(yearsofexperience) <= 8
  )

cat("Num samples: ", nrow(salaries_df), "\n")

# (!!) NOTE: all monetary quantities from levels.fyi are stored in USD to
# facilitate comparison of salaries in various countries.
p50 <- median(as.numeric(salaries_df$totalyearlycompensation))
cat("Median: ", p50, "k USD\n")
cat("Standard deviation: ", sd(as.numeric(salaries_df$totalyearlycompensation)), "k USD\n")

# Therefore we need to apply the approximate USD-to-CAD conversion rate as of
# September, 2021.
kUsdToCad <- 1.2647903

# 90-th percentile among SWEs in Canada with 7-8 YOE => ~260k CAD / yr
cat(
  "The percentile: ",
  ecdf(kUsdToCad * as.numeric(salaries_df$totalyearlycompensation))(260 * 1.1 + 6.5) * 100,
  "%\n"
)
